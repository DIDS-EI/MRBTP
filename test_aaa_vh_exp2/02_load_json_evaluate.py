import json
import sys
import time
import random
import math
import numpy as np
import pandas as pd
from mabtpg.algo.llm_client.llms.gpt3 import LLMGPT3
import gymnasium as gym
from mabtpg import MiniGridToMAGridEnv
from minigrid.core.world_object import Ball, Box,Door,Key
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

def bind_bt(bt_list):
    from mabtpg.behavior_tree.behavior_tree import BehaviorTree
    # new
    # bt_list = []
    # for i, agent in enumerate(planning_algorithm.planned_agent_list):
    #     bt = BehaviorTree(btml=btml_list[i], behavior_lib=behavior_lib[i])
    #     bt_list.append(bt)
    for i in range(env.num_agent):
        bt_list[i].save_btml(f"robot-{i}.bt")
        if bt_draw:
            bt_list[i].draw(file_name=f"agent-{i}")
    # bind the behavior tree to agents
    for i, agent in enumerate(env.agents):
        agent.bind_bt(bt_list[i])


# 定义记录和计算平均值的函数
def record_data(data_id,with_comp_action, use_comp_subtask_chain, use_atom_subtask_chain,
                done, env_steps, agents_steps, communication_times,CABTP_expanded_num, dmr_record_expanded_num, CABTP_expanded_time, dmr_expanded_time):

    details = {
        'data_id':data_id,
        'with_comp_action': with_comp_action,
        'use_comp_subtask_chain': use_comp_subtask_chain,
        'use_atom_subtask_chain': use_atom_subtask_chain,
        'done': done,
        'env_steps': env_steps,
        'agents_steps': agents_steps,
        "communication_times": communication_times,
        'CABTP_expanded_num': CABTP_expanded_num,
        'dmr_record_expanded_num': dmr_record_expanded_num,
        'total_expanded_num': CABTP_expanded_num + dmr_record_expanded_num,
        'CABTP_expanded_time': CABTP_expanded_time,
        'dmr_expanded_time': dmr_expanded_time,
        'total_expanded_time': CABTP_expanded_time + dmr_expanded_time
    }

    all_details.append(details)
    return details


# json_path = "vh1.json"

# json_type = "homo"
# json_type = "hete"
json_type = "half"


json_path = f"vh_{json_type}.json"
with open(json_path, 'r') as file:
    json_datasets = json.load(file)

# for with_comp_action in [False, True]:
#     for use_comp_subtask_chain in [False, True]:
#         for use_atom_subtask_chain in [False, True]:


verbose = False

# 用于记录所有数据的列表
all_details = []
average_details = []

# comp = False
# for with_comp_action in [comp]:
#     for use_comp_subtask_chain in [comp]:
#         for use_atom_subtask_chain in [False]:

for with_comp_action in [False, True]:
    for use_comp_subtask_chain in [False, True]:
        if with_comp_action==False and use_comp_subtask_chain==True:
            continue
        for use_atom_subtask_chain in [False, True]:

            print_colored(f"=========  comp_action={with_comp_action} comp_subtask_chain={use_comp_subtask_chain}  atom_subtask_chain={use_atom_subtask_chain}==============",color="purple")

            for _,json_data in enumerate(json_datasets[:]):

                data_id = json_data['id']
                print_colored(f"========= data_id: {data_id} ===============","blue")
                goal = frozenset(json_data["goal"])
                start = set(json_data["init_state"])
                objects = json_data["objects"]
                action_space = json_data["action_space"]
                num_agent = len(action_space)

                for i in range(num_agent):
                    start.add(f"IsRightHandEmpty(agent-{i})")
                    start.add(f"IsLeftHandEmpty(agent-{i})")
                start = frozenset(start)


                # #########################
                # Initialize Environment
                # #########################
                env = VHCompEnv(num_agent=num_agent, goal=goal, start=start)
                env.objects = objects
                env.filter_objects_to_get_category(objects)

                env.with_comp_action = with_comp_action # 是否有組合動作
                env.use_comp_subtask_chain = use_comp_subtask_chain  # 是否使用任務鏈

                env.use_atom_subtask_chain = use_atom_subtask_chain # 是否使用任務鏈


                bt_draw = verbose


                # #####################
                # get action model
                # #####################
                behavior_lib_path = f"{root_path}/envs/virtualhome/behavior_lib"
                behavior_lib = BehaviorLibrary(behavior_lib_path)

                agents_act_cls_ls = [[] for _ in range(num_agent)]
                for i,act_cls_name_ls in enumerate(action_space):
                    for act_cls_name in act_cls_name_ls:
                        act_cls = type(f"{act_cls_name}", (behavior_lib["Action"][act_cls_name],), {})
                        agents_act_cls_ls[i].append(act_cls)

                for i, agent in enumerate(env.agents):
                    agent.behavior_dict = {
                        "Action": agents_act_cls_ls[i]+[behavior_lib["Action"]['SelfAcceptTask'],behavior_lib["Action"]['FinishTask']],
                        "Condition": behavior_lib["Condition"].values(),
                    }
                    agent.create_behavior_lib()
                action_model = env.create_action_model()


                # #########################
                # Composition Action
                # Pre-plan get BTML and PlanningAction
                # #########################
                composition_action = []
                comp_btml_ls=None
                comp_planning_act_ls = None
                CABTP_expanded_num = 0
                CABTP_expanded_time = 0
                if "composition_action" in json_data:
                    composition_action = json_data["composition_action"]

                    if env.with_comp_action:
                        cap = CompositeActionPlanner(action_model, composition_action, env=env)
                        cap.get_composite_action()
                        # [[WalkToOpen(agent-0,fridge), WalkToOpen(agent-0,milk)],[]]
                        comp_planning_act_ls = cap.planning_ls
                        # [[],[],[]]
                        comp_btml_ls = cap.btml_ls
                        CABTP_expanded_num = cap.expanded_num
                        CABTP_expanded_time = cap.expanded_time

                        print("comp_planning_act_ls:",comp_planning_act_ls)
                        print("comp_btml_ls:", comp_btml_ls)

                        for i in range(env.num_agent):
                            action_model[i].extend(comp_planning_act_ls[i])
                            action_model[i] = sorted(action_model[i], key=lambda x: x.cost)  # 不加也有问题？完全异构的第一个例子


                # #########################
                # Run Decentralized multi-agent BT algorithm
                # #########################
                # print_colored(f"Start Multi-Robot Behavior Tree Planning...", color="green")
                start_time = time.time()
                from mabtpg.btp.DMR import DMR
                dmr = DMR(env, goal, start, action_model, num_agent, with_comp_action=env.with_comp_action,
                          save_dot=bt_draw)  # False 也还需要再调试
                dmr.planning()

                # Convert to BT and bind the BT to the agent
                behavior_lib = [agent.behavior_lib for agent in env.agents]
                dmr.get_btml_and_bt_ls(behavior_lib=behavior_lib, comp_btml_ls=comp_btml_ls, comp_planning_act_ls=comp_planning_act_ls)
                bind_bt(dmr.bt_ls)


                # calculate time and expanded num
                # dmr.record_expanded_num
                # dmr.expanded_time



                # #########################
                # Simulation
                # #########################
                print_colored(f"start: {start}", "blue")
                env.print_ticks = verbose
                env.verbose = verbose
                env.reset()
                done = False
                max_env_step = 50
                env_steps = 0
                new_env_step = 0
                agents_steps = 0
                obs = set(start)
                env.state = obs
                while not done:
                    obs, done, _, _, agents_one_step, _ = env.step()
                    env_steps += 1
                    agents_steps += agents_one_step
                    # if env_steps % 50 == 0:
                    if verbose:
                        print_colored(f"========= env_steps: {env_steps} ===============",
                                      "blue")
                        print_colored(f"state: {obs}", "blue")
                    if obs >= goal:
                        done = True
                        break
                    if env_steps >= max_env_step:
                        break
                print(f"\ntask finished!")
                print_colored(f"goal:{goal}", "blue")
                if obs>=goal:
                    print_colored(f"obs>=goal: {obs >= goal}",color="green")
                else:
                    print_colored(f"obs>=goal: {obs >= goal}", color="red")
                    sys.exit()
                agents_steps = agents_steps/num_agent
                communication_times = env.communication_times
                print("done:",done,"env_steps:",env_steps, "agent step:",agents_steps,"comm:",communication_times)
                print("CABTP expanded num:",CABTP_expanded_num, "expanded num:",dmr.record_expanded_num,"total expanded num:",CABTP_expanded_num+dmr.record_expanded_num)
                print("CABTP time:", CABTP_expanded_time, "expanded time:",dmr.expanded_time,"total time",CABTP_expanded_time+dmr.expanded_time)
                print("expanded time:",dmr.expanded_time)

                details = record_data(data_id,with_comp_action, use_comp_subtask_chain, use_atom_subtask_chain, done,
                                      env_steps, agents_steps, communication_times,
                                      CABTP_expanded_num, dmr.record_expanded_num, CABTP_expanded_time, dmr.expanded_time)

            # 计算每种配置的平均值
            df_details = pd.DataFrame(all_details)
            config_details = df_details[
                (df_details['with_comp_action'] == with_comp_action) &
                (df_details['use_comp_subtask_chain'] == use_comp_subtask_chain) &
                (df_details['use_atom_subtask_chain'] == use_atom_subtask_chain)
                ]

            avg_details = config_details.mean().to_dict()
            avg_details.update({
                'with_comp_action': with_comp_action,
                'use_comp_subtask_chain': use_comp_subtask_chain,
                'use_atom_subtask_chain': use_atom_subtask_chain
            })

            average_details.append(avg_details)


# 保存所有详细数据到CSV
df_all_details = pd.DataFrame(all_details)
df_all_details.to_csv(f'{json_type}_details_data.csv', index=False)

# 保存所有平均值数据到新的CSV
df_avg_details = pd.DataFrame(average_details)
df_avg_details.to_csv(f'{json_type}_average_data.csv', index=False)

# 定义并打印总结表格的函数

# 打印平均值情况
print("Formatted table:")
print_summary_table(df_avg_details, formatted=True)

print("\nCSV formatted table:")
print_summary_table(df_avg_details, formatted=False)










# record with_comp_action,use_comp_subtask_chain,use_atom_subtask_chain
# env_steps,agents_steps,
# print("CABTP expanded num:",CABTP_expanded_num, "expanded num:",dmr.record_expanded_num,"total expanded num:",CABTP_expanded_num+dmr.record_expanded_num)
# print("CABTP time:", CABTP_expanded_time, "expanded time:",dmr.expanded_time,"total time",CABTP_expanded_time+dmr.expanded_time)
# print("expanded time:",dmr.expanded_time)




