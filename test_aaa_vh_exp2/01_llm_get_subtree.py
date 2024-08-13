import json
import csv
import os
import re
from openai import OpenAI
import openai
import time
import copy
from mabtpg.utils.tools import print_colored
from mabtpg.algo.llm_client.llms.gpt4_act import LLMGPT4
from mabtpg.utils import get_root_path
from mabtpg import BehaviorLibrary
root_path = get_root_path()
from itertools import permutations
import time
from mabtpg.utils.composite_action_tools import CompositeActionPlanner
from mabtpg.utils.tools import print_colored,filter_action_lists
from mabtpg.envs.gridenv.minigrid_computation_env.mini_comp_env import MiniCompEnv
from mabtpg.envs.virtualhome.envs.vh_computation_env import VHCompEnv
from mabtpg.envs.numerical_env.numsim_tools import create_directory_if_not_exists, print_action_data_table,print_summary_table
from itertools import chain
from enum import Enum
from typing import Union
from pydantic import BaseModel
# 加载 json 文件，依次询问大模型，写入 json 文件
# 得到 new json 和 时间记录 csv 以及有无反馈下的 正确率


# Initialize the counter dictionary
count_dict = {
    'In(obj, contain)': 0,
    'On(obj, surface)': 0,
    'IsOpen(obj)': 0,
    'IsClose(obj)': 0,
    'IsSwitchOn(obj)': 0,
    'IsSwitchOff(obj)': 0
}
def count_conditions(goal):
    # Iterate through the goal set and count different conditions
    for condition in goal:
        if 'IsIn' in condition:
            count_dict['In(obj, contain)'] += 1
        elif 'IsOn' in condition:
            count_dict['On(obj, surface)'] += 1
        elif 'IsOpen' in condition:
            count_dict['IsOpen(obj)'] += 1
        elif 'IsClose' in condition:
            count_dict['IsClose(obj)'] += 1
        elif 'IsSwitchedOn' in condition:
            count_dict['IsSwitchOn(obj)'] += 1
        elif 'IsSwitchedOff' in condition:
            count_dict['IsSwitchOff(obj)'] += 1

    return count_dict


default_prompt_file = f"conditions_and_actions.txt"
with open(default_prompt_file, 'r', encoding="utf-8") as f:
    default_prompt = f.read().strip()

def get_prompt(json_data,num_agent):
    prompt = default_prompt + f'''

[Task Information]
{new_json_data}
    '''

    return prompt




# json_type = "homo_30"
# json_type = "half_30"
json_type = "hete_30"
json_path = f"vh_{json_type}.json"
with open(json_path, 'r') as file:
    json_datasets = json.load(file)

output_json_name = f"vh_llm4_{json_type}_1_supplement.json"
output_csv_name = f"vh_llm4_{json_type}_1_supplement.csv"

# initial json file
if not os.path.exists(output_json_name):
    with open(output_json_name, 'w') as json_file:
        json.dump([], json_file)
# initial csv file
if not os.path.exists(output_csv_name):
    with open(output_csv_name, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["data_id", "goal", "init_state", "objects", "action_space", "llm_time","reflect_times",
                                            "llm_output1","reflect1","llm_output2","reflect2","llm_output3","reflect3","llm_output4"])
        writer.writeheader()



for _,json_data in enumerate(json_datasets[:]):
    data_id = json_data['id']
    print_colored(f"=============================== data_id: {data_id} =========================================","purple")

    goal = frozenset(json_data["goal"])
    start = set(json_data["init_state"])
    objects = json_data["objects"]
    action_space = json_data["action_space"]
    num_agent = len(action_space)

    count_conditions(goal)
    continue


    for i in range(num_agent):
        start.add(f"IsRightHandEmpty(agent-{i})")
        start.add(f"IsLeftHandEmpty(agent-{i})")
    start = frozenset(start)

    new_json_data = {
        "id": data_id,
        'goal': list(goal),
        'init_state': list(start),
        "objects": objects,
        'action_space': action_space
    }

    # #########################
    # Initialize Environment
    # #########################
    env = VHCompEnv(num_agent=num_agent, goal=goal, start=start)
    env.objects = objects
    env.filter_objects_to_get_category(objects)

    env.with_comp_action = True  # 是否有組合動作
    env.use_comp_subtask_chain = False  # 是否使用任務鏈

    env.use_atom_subtask_chain = False  # 是否使用任務鏈
    bt_draw = False

    # #####################
    # get action model
    # #####################
    behavior_lib_path = f"{root_path}/envs/virtualhome/behavior_lib"
    behavior_lib = BehaviorLibrary(behavior_lib_path)

    agents_act_cls_ls = [[] for _ in range(num_agent)]
    for i, act_cls_name_ls in enumerate(action_space):
        for act_cls_name in act_cls_name_ls:
            act_cls = type(f"{act_cls_name}", (behavior_lib["Action"][act_cls_name],), {})
            agents_act_cls_ls[i].append(act_cls)

    for i, agent in enumerate(env.agents):
        agent.behavior_dict = {
            "Action": agents_act_cls_ls[i] + [behavior_lib["Action"]['SelfAcceptTask'],
                                              behavior_lib["Action"]['FinishTask']],
            "Condition": behavior_lib["Condition"].values(),
        }
        agent.create_behavior_lib()
    action_model = env.create_action_model()


    # get prompt
    prompt = get_prompt(new_json_data,num_agent)

#    '''
# 1. Based on each task's goal, start, and the action spaces of different robots, design all possible task-related composite actions [multi_robot_subtree_ls] for each robot. It's okay if many composite actions are repeated.
# 2. [multi_robot_subtree_ls] is a list where each entry contains a dictionary [subtree_dict] of all task-related composite actions a robot can perform. It's okay if many composite actions are repeated.
# 3. In [subtree_dict], the keys are composite action names, and the values are the atomic actions that make up each composite action. Atomic actions are formed by combining action predicates with objects. The sequence of atomic actions within each composite action is ordered and related, where the add effect of each atomic action serves as the precondition for the next.
# 4. Refer to [Example] and use the current [Task Information] to provide the task-related composite actions [multi_robot_subtree_ls] for each robot. The current number of robots is {num_agent}, meaning [multi_subtree_list] has {num_agent} dictionaries.
# 5. For each robot, provide as many task-related composite actions as possible from the actions it can perform. Each [subtree_dict] can contain multiple key-value pairs, typically including 2-4 actions.
# 6. The length of multi_subtree_list corresponds to the number of robots, which equals the number of action lists contained in action_space. The current number of robots is {num_agent}.
# 7
    # '''

    prompt += f'''
    [Systems]
1. Based on each task's goal, start, and the action spaces of different robots, design all possible task-related composite actions [multi_robot_subtree_ls] for each robot. It's okay if many composite actions are repeated.
2. [multi_robot_subtree_ls] is a list where each entry contains a dictionary [subtree_dict] of all task-related composite actions a robot can perform. It's okay if many composite actions are repeated.
3. In [subtree_dict], the keys are composite action names, and the values are the atomic actions that make up each composite action. Atomic actions are formed by combining action predicates with objects. The sequence of atomic actions within each composite action is ordered and related, where the add effect of each atomic action serves as the precondition for the next.
4. Refer to [Example] and use the current [Task Information] to provide the task-related composite actions [multi_robot_subtree_ls] for each robot. The current number of robots is {num_agent}, meaning [multi_subtree_list] has {num_agent} dictionaries.
5. For each robot, provide as many task-related composite actions as possible from the actions it can perform. Each [subtree_dict] can contain multiple key-value pairs, typically including 1-5 actions.
6. The length of multi_subtree_list corresponds to the number of robots, which equals the number of action lists contained in action_space. The current number of robots is {num_agent}.
7. The number of robots in this task is {num_agent}, meaning multi_subtree_list contains {num_agent} dictionaries. Each dictionary includes 1-5 key-value pairs.
'''


    # class Action(str, Enum):
    #     Walk_self_toy = "Walk(self,toy)"
    #     RightGrab_self_toy = "RightGrab(self,toy)"
    actions_name_str_ls=[]
    flattened_unique = list(set(chain.from_iterable(action_model)))
    for planning_action in flattened_unique:
        action_modified_str = re.sub(r'agent-\d+', 'self', planning_action.name)
        actions_name_str_ls.append(action_modified_str)
    actions_name_str_ls = list(set(actions_name_str_ls))


    # get result
    class Action(str, Enum):
        # Walk_self_toy = "Walk(self,toy)"
        # RightGrab_self_toy = "RightGrab(self,toy)"
        actions_name_str_ls = actions_name_str_ls

    class AgentSubtreeDict(BaseModel):
        """
        `subtree_dict` contains multiple composite action pairs, typically including 2-4 key-value pairs.
        """
        subtree_dict: dict[str, list[Action]]

    # class AgentSubtreeList(BaseModel):
    #     # """
    #     # `subtree_dict` 包含多个组合动作对，即包括多个键值对，一般2-4个键值对
    #     # """
    #     agent_subtree_list: list[AgentSubtreeDict]

    class Query(BaseModel):
        """
        The length of multi_subtree_list corresponds to the number of robots, which equals the number of action lists contained in action_space.
        """
        multi_subtree_list: list[AgentSubtreeDict]


    tools = [openai.pydantic_function_tool(Query)]
    llm = LLMGPT4()

    history_dic  = {
        "llm_output1": None,
        "reflect1": None,
        "llm_output2": None,
        "reflect2": None,
        "llm_output3": None,
        "reflect3": None,
        "llm_output4": None
    }

    messages = [{"role": "system", "content": "You are a helpful assistant. Please provide as many task-related combined actions as possible for each robot by calling the query function, according to the task details."}]
    messages.append({"role": "user", "content": prompt})

    multi_subtree_list = []
    reflect_times = 0
    llm_time=0
    start_time = time.time()
    while reflect_times<3:

        if reflect_times!=0:
            print_colored(
                f" reflect: {reflect_times} ", "yellow")

        start_time = time.time()
        res_msg = llm.tool_request(messages, tools=tools)
        llm_time = time.time() - start_time
        print("Times:", llm_time)

        multi_subtree_list = eval(res_msg)["multi_subtree_list"]
        history_dic[f"llm_output{reflect_times+1}"]= multi_subtree_list
        print(multi_subtree_list)

        # check if need reflect
        reflect_prompt = ""
        if len(multi_subtree_list) < num_agent:
            reflect_prompt = f'''
            The number of dictionaries in the [multi_subtree_list] you provided should equal the number of {num_agent}. Please regenerate the composite action dictionaries for each robot. Each of the {num_agent} dictionaries in the list should contain 2-4 key-value pairs. Please revise accordingly.
            '''
            messages.append({"role": "user", "content": reflect_prompt})
            history_dic[f"reflect{reflect_times+1}"]=reflect_prompt
            reflect_times+=1
            continue

        # hete
        break

        # heto
        # need_reflect = True
        # for subtree_list in multi_subtree_list:
        #     if len(subtree_list)>1:
        #         need_reflect = False
        # if not need_reflect:
        #     break

        # messages.append({"role": "assistant", "content": res_msg})
        # reflect_prompt += f'''
        # The number of robots in this task is {num_agent}, meaning multi_subtree_list contains {num_agent} dictionaries. Each dictionary includes 4 key-value pairs.
        # You should provide 2-4 combined actions for each robot instead of just one. Each of the {num_agent} dictionaries in the list should contain 2-4 key-value pairs. Please revise accordingly.
        # '''
        # messages.append({"role": "user", "content": reflect_prompt})
        # history_dic[f"reflect{reflect_times+1}"]=reflect_prompt
        # reflect_times+=1

    history_dic[f"llm_output{reflect_times + 1}"] = multi_subtree_list
    # print(multi_subtree_list)

    new_json_data["total_time"] = time.time() - start_time
    new_json_data["multi_robot_subtree_ls"] = multi_subtree_list
    new_json_data["llm_time"] = llm_time
    new_json_data["reflect_times"] = reflect_times


    # 读取JSON文件
    with open(output_json_name, 'r+') as json_file:
        try:
            existing_data = json.load(json_file)
        except json.JSONDecodeError:  # 捕获 JSON 解码错误
            existing_data = []  # 如果文件为空或损坏，则初始化为空列表
        # 更新数据并写入文件
        existing_data.append(new_json_data)
        json_file.seek(0)
        json.dump(existing_data, json_file, indent=4)

    # 写入CSV文件
    with open(output_csv_name, 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file,
                                fieldnames=["data_id", "goal", "init_state", "objects", "action_space", "llm_time","reflect_times",
                                            "llm_output1","reflect1","llm_output2","reflect2","llm_output3","reflect3","llm_output4"])
        writer.writerow({
            "data_id": data_id,
            "goal": list(goal),
            "init_state": list(start),
            "objects": objects,
            "action_space": action_space,
            "llm_time": llm_time,
            "reflect_times": reflect_times,
            "llm_output1": str(history_dic["llm_output1"]),
            "reflect1": str(history_dic["reflect1"]),
            "llm_output2": str(history_dic["llm_output2"]),
            "reflect2": str(history_dic["reflect2"]),
            "llm_output3": str(history_dic["llm_output3"]),
            "reflect3": str(history_dic["reflect3"]),
            "llm_output4": str(history_dic["llm_output4"])
        })



print(count_dict)







