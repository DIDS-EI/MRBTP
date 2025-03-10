import sys
import os
project_parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(project_parent_dir)
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), './'))
sys.path.append(project_dir)

import json
import csv
import os
import re
from openai import OpenAI
import openai
import time
import copy

from mabtpg.utils.tools import print_colored
from mabtpg.algo.llm_client.llms.gpt3_act import LLMGPT3
from mabtpg.algo.llm_client.llms.gpt4o_act import LLMGPT4o
from mabtpg.algo.llm_client.llms.gpt4 import LLMGPT4
from mabtpg.utils import get_root_path
from mabtpg import BehaviorLibrary
root_path = get_root_path()
from itertools import permutations
import time
from mabtpg.utils.composite_action_tools import CompositeActionPlanner
from mabtpg.utils import parse_predicate_logic
from mabtpg.utils.tools import print_colored,filter_action_lists
from mabtpg.envs.virtualhome.envs.vh_computation_env import VHCompEnv
from itertools import chain
from enum import Enum
from pydantic import BaseModel

# Load JSON files, sequentially query the large model, and write to JSON files
# Obtain the new JSON and time record CSV, and the accuracy with and without feedback

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


default_prompt_file = os.path.join(root_path, "../test_experiment/exp2_subtree_llms/code/prompt.txt")
with open(default_prompt_file, 'r', encoding="utf-8") as f:
    default_prompt = f.read().strip()

def get_prompt(json_data,num_agent):
    prompt = default_prompt + f'''

[Task Information]
{new_json_data}
    '''

    return prompt


need_record_reflect = True

json_type = "homo_25"
# json_type = "half_25"
# json_type = "hete_25"
# json_path = f"data/vh_{json_type}.json"
json_path = os.path.join(root_path, "../test_experiment/exp2_subtree_llms/code/data", f"vh_{json_type}.json")
with open(json_path, 'r') as file:
    json_datasets = json.load(file)

model = "gpt3"
# model = "gpt4o"

# output_json_name = f"llm_data/vh_{model}_{json_type}_reflect_tmp.json"
# output_csv_name = f"llm_data/vh_{model}_{json_type}_reflectt_tmp.csv"
output_json_name = os.path.join(root_path, "../test_experiment/exp2_subtree_llms/code/llm_data", f"vh_{model}_{json_type}_reflect_tmp.json")
output_csv_name = os.path.join(root_path, "../test_experiment/exp2_subtree_llms/code/llm_data", f"vh_{model}_{json_type}_reflectt_tmp.csv")

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

    # count_conditions(goal)
    # continue


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

    env.with_comp_action = True  # Whether composite actions are involved
    env.use_comp_subtask_chain = False  # Whether to use task chains

    env.use_atom_subtask_chain = False  # Whether to use atomic task chains
    bt_draw = False

    # #####################
    # Get action model
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
    prompt += f'''
    [Systems]
    1. For each task, generate all possible composite actions for each robot based on its goals, initial state, and available action space. Repetition of composite actions is permissible. 
    2. [multi\_robot\_subtree\_ls] is a list where each entry is a dictionary [subtree\_dict] containing all task-related composite actions for a robot. Keys in [subtree\_dict] are composite action names, and values are sequences of atomic actions, ordered such that each action’s effect serves as the precondition for the next. Using the current [Task Information] and [Example], construct [multi\_robot\_subtree\_ls] for each robot.
    3. The length of \[multi\_subtree\_list] equals the number of robots and corresponds to the number of action lists in [action\_space]. With  {num_agent} robots, [multi\_subtree\_list] contains {num_agent} dictionaries, each with 1-5 key-value pairs.
    '''

#     prompt += f'''
#     [Systems]
# 1. Based on each task's goal, start, and the action spaces of different robots, design all possible task-related composite actions [multi_robot_subtree_ls] for each robot. It's okay if many composite actions are repeated.
# 2. [multi_robot_subtree_ls] is a list where each entry contains a dictionary [subtree_dict] of all task-related composite actions a robot can perform. It's okay if many composite actions are repeated.
# 3. In [subtree_dict], the keys are composite action names, and the values are the atomic actions that make up each composite action. Atomic actions are formed by combining action predicates with objects. The sequence of atomic actions within each composite action is ordered and related, where the add effect of each atomic action serves as the precondition for the next.
# 4. Refer to [Example] and use the current [Task Information] to provide the task-related composite actions [multi_robot_subtree_ls] for each robot. The current number of robots is {num_agent}, meaning [multi_subtree_list] has {num_agent} dictionaries.
# 5. For each robot, provide as many task-related composite actions as possible from the actions it can perform. Each [subtree_dict] can contain multiple key-value pairs, typically including 1-5 actions.
# 6. The length of multi_subtree_list corresponds to the number of robots, which equals the number of action lists contained in action_space. The current number of robots is {num_agent}.
# 7. The number of robots in this task is {num_agent}, meaning multi_subtree_list contains {num_agent} dictionaries. Each dictionary includes 1-5 key-value pairs.
# '''


    # Extract action names and normalize for model input
    actions_name_str_ls=[]
    flattened_unique = list(set(chain.from_iterable(action_model)))
    for planning_action in flattened_unique:
        action_modified_str = re.sub(r'agent-\d+', 'self', planning_action.name)
        actions_name_str_ls.append(action_modified_str)
    actions_name_str_ls = list(set(actions_name_str_ls))


    # Class definitions for structured responses
    class Action(str, Enum):
        actions_name_str_ls = actions_name_str_ls

    class AgentSubtreeDict(BaseModel):
        """
        `subtree_dict` contains multiple composite action pairs, typically including 2-4 key-value pairs.
        """
        subtree_dict: dict[str, list[Action]]

    class Query(BaseModel):
        """
        The length of multi_subtree_list corresponds to the number of robots, which equals the number of action lists contained in action_space.
        """
        multi_subtree_list: list[AgentSubtreeDict]


    tools = [openai.pydantic_function_tool(Query)]
    # llm = LLMGPT4()
    # llm = LLMGPT3()

    if model=="gpt4o":
        llm = LLMGPT4o()
    elif model=="gpt3":
        llm=LLMGPT3()
    elif model=="gpt4":
        llm=LLMGPT4()
    # llm = LLMGPT3()

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
        if need_record_reflect:
            new_json_data[f"llm_output{reflect_times}"] = multi_subtree_list
        print(multi_subtree_list)

        # check if need reflect
        num_feedback_items = 1
        feedback_prompt = ""

        # Check for grammatical errors.
        # objs、actions
        llm_objs = set()
        llm_act = set()
        for subtree_dic in multi_subtree_list:
            for atom_act_ls in subtree_dic.values():
                for act in atom_act_ls:
                    cls_name, args = parse_predicate_logic(act)
                    llm_objs |= set(args)
                    llm_act |= set(act)
        not_exists_objs = llm_objs & (set(objects)|{"self"})
        not_exists_act_pred = llm_act & (set(actions_name_str_ls))
        if not_exists_objs!=set():
            feedback_prompt += f"{num_feedback_items}. The object(s) {not_exists_objs} do(es) not exist and must be an element(s) of the set {set(objects)}."
            num_feedback_items += 1
        if not_exists_act_pred!=set():
            feedback_prompt += f"{num_feedback_items}. The action predicates {not_exists_act_pred} either do not exist or are incorrectly formatted. They must be part of the {set((actions_name_str_ls))} set."
            num_feedback_items += 1

        # Check for len(multi_subtree_list) == num_agent.
        if len(multi_subtree_list) < num_agent:
            feedback_prompt+= (f"{num_feedback_items}. The number of robots involved in this task is {num_agent}, "
                               f"which implies that the [multi_subtree_list] should contain {num_agent} dictionaries. "
                               f"Each of these dictionaries should have 1-4 key-value pairs. Please revise accordingly.")
            num_feedback_items += 1

        if num_feedback_items !=1:
            messages.append({"role": "user", "content": feedback_prompt})
            history_dic[f"reflect{reflect_times+1}"]=feedback_prompt
            reflect_times+=1
            continue

        # Check for Subtree Pre-Planning
        # Subree Pre-Planning
        # Collect and use together
        for ls_i, act_cls_dic in enumerate(multi_subtree_list):
            for key, act_name_ls in act_cls_dic.items():
                for act_j, act_name in enumerate(act_name_ls):
                    if re.search(r'agent-\d+', act_name):
                        action_modified_str = re.sub(r'agent-\d+', 'self', act_name)
                        act_cls_dic[key][act_j] = action_modified_str

        # Collect and use together
        if model!="gpt3":
            total_dic = {}
            for ls_i, act_cls_dic in enumerate(multi_subtree_list):
                for key, act_name_ls in act_cls_dic.items():
                    ket_name = key.replace("_", "").replace("(", "").replace(")", "").replace(" ", "")
                    total_dic[ket_name] = act_name_ls
            composition_action = [[] for i in range(num_agent)]
            for i in range(num_agent):
                composition_action[i] = total_dic
        else:
            total_dic = {}
            for subtree_dict_dict in multi_subtree_list:
                subtree_dict = subtree_dict_dict.values()
                first_dict = next(iter(subtree_dict)) # dict_values
                print("first_dict:",first_dict)
                for key, act_name_ls in first_dict.items():
                    ket_name = key.replace("_", "").replace("(", "").replace(")", "").replace(" ", "")
                    total_dic[ket_name] = act_name_ls
        
        if model!="gpt3":
            for key, value in total_dic.values():
                cap = CompositeActionPlanner(multi_subtree_list, action_model)
                success,msg = cap.get_single_agent_composite_action(key,value,-1,action_model)

                if not success:
                    feedback_prompt += (f"{num_feedback_items}. {key} cannot be pre-planned. {msg}")
                    num_feedback_items += 1
        else:
            for key, value in total_dic.items():
                cap = CompositeActionPlanner(multi_subtree_list, action_model)
                success,msg = cap.get_single_agent_composite_action(key,value,-1,action_model)

                if not success:
                    feedback_prompt += (f"{num_feedback_items}. {key} cannot be pre-planned. {msg}")
                    num_feedback_items += 1
        
        
        # for gpt-3.5， may error:ValueError: too many values to unpack (expected 2)
        # so 2024 12 14
        # try:
        #     for key, value in total_dic.values():
        #         cap = CompositeActionPlanner(multi_subtree_list, action_model)
        #         success,msg = cap.get_single_agent_composite_action(key,value,-1,action_model)

        #         if not success:
        #             feedback_prompt += (f"{num_feedback_items}. {key} cannot be pre-planned. {msg}")
        #             num_feedback_items += 1
        # except ValueError as e:
        #     if str(e) == "too many values to unpack (expected 2)":
        #         # 特殊处理，当遇到特定的ValueError时
        #         for inner_dict in total_dic.values():
        #             for key, value_list in inner_dict.items():
        #                 cap = CompositeActionPlanner(multi_subtree_list, action_model[0])
        #                 success, msg = cap.get_single_agent_composite_action(key, value_list, -1, action_model[0])

        #                 if not success:
        #                     feedback_prompt += (f"{num_feedback_items}. {key} cannot be pre-planned. {msg}")
        #                     num_feedback_items += 1
        # # # so 2024 12 14


        if num_feedback_items!=1:
            messages.append({"role": "user", "content": feedback_prompt})
            history_dic[f"reflect{reflect_times+1}"] = feedback_prompt
            reflect_times+=1
        else:
            break


        # if len(multi_subtree_list) < num_agent:
        #     reflect_prompt = f'''
        #     The number of dictionaries in the [multi_subtree_list] you provided should equal the number of {num_agent}. Please regenerate the composite action dictionaries for each robot. Each of the {num_agent} dictionaries in the list should contain 2-4 key-value pairs. Please revise accordingly.
        #     '''
        #     messages.append({"role": "user", "content": reflect_prompt})
        #     history_dic[f"reflect{reflect_times+1}"]=reflect_prompt
        #     reflect_times+=1
        #     continue
        #
        # # hete
        # # break
        #
        # # heto
        # need_reflect = True
        # for subtree_list in multi_subtree_list:
        #     if len(subtree_list)>1:
        #         need_reflect = False
        # if not need_reflect:
        #     break
        #
        # messages.append({"role": "assistant", "content": res_msg})
        # reflect_prompt += f'''
        # The number of robots in this task is {num_agent}, meaning multi_subtree_list contains {num_agent} dictionaries. Each dictionary includes 4 key-value pairs.
        # You should provide 2-4 combined actions for each robot instead of just one. Each of the {num_agent} dictionaries in the list should contain 2-4 key-value pairs. Please revise accordingly.
        # '''
        # messages.append({"role": "user", "content": reflect_prompt})
        # history_dic[f"reflect{reflect_times+1}"] = reflect_prompt
        # messages.append({"role": "user", "content": feedback_prompt})
        # history_dic[f"reflect{reflect_times+1}"] = feedback_prompt
        # reflect_times+=1

    history_dic[f"llm_output{reflect_times + 1}"] = multi_subtree_list
    # print(multi_subtree_list)

    new_json_data["total_time"] = time.time() - start_time
    new_json_data["multi_robot_subtree_ls"] = multi_subtree_list
    new_json_data["llm_time"] = llm_time
    new_json_data["reflect_times"] = reflect_times


    # Read JSON file
    with open(output_json_name, 'r+') as json_file:
        try:
            existing_data = json.load(json_file)
        except json.JSONDecodeError:  # Catch JSON decoding error
            existing_data = []  # If the file is empty or corrupted, initialize it as an empty list
        # Update data and write bak to the file
        existing_data.append(new_json_data)
        json_file.seek(0)
        json.dump(existing_data, json_file, indent=4)

    # Write to CSV file
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







