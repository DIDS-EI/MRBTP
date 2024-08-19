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
from mabtpg.envs.numerical_env.numsim_tools import create_directory_if_not_exists, print_action_data_table,print_summary_table



behavior_lib_path = f"{root_path}/envs/gridenv/minigrid_computation_env/behavior_lib"
behavior_lib = BehaviorLibrary(behavior_lib_path)

random.seed(0)
np.random.seed(0)

# 11 22 33 44
# def generate_agents_actions(num_cls_ls, num_agent, homogeneity_probability):
#     agents_actions = [[] for _ in range(num_agent)]
#
#     # 计算需要分配给的智能体数量
#     num_agents_to_assign = math.ceil(homogeneity_probability * num_agent)
#     if num_agents_to_assign < 1:
#         num_agents_to_assign = 1
#
#     agent_index = 0
#     # 按序分配给智能体
#     for cls_index in range(num_cls_ls):
#         for i in range(num_agents_to_assign):
#             agents_actions[agent_index].append(cls_index)
#             agent_index = (agent_index+1) % num_agent
#     return agents_actions

# def generate_agents_actions(num_cls_index_ls, num_agent, homogeneity_probability):
#     agents_actions = [[] for _ in range(num_agent)]
#
#     # 计算需要分配给的智能体数量
#     num_agents_to_assign = math.ceil(homogeneity_probability * num_agent)
#     if num_agents_to_assign < 1:
#         num_agents_to_assign = 1
#
#     for times in range(num_agents_to_assign):
#         agent_index = times # 每次从上次结束的后一个开始
#         for cls_index in range(num_cls_index_ls):
#             agents_actions[agent_index].append(cls_index)
#             agent_index = (agent_index + 1) % num_agent
#     return agents_actions




# 第一个按照顺序分，其它的随机分
# def generate_agents_actions(num_cls_index_ls, num_agent, homogeneity_probability):
#     agents_actions = [[] for _ in range(num_agent)]
#
#     # 计算需要分配给的智能体数量
#     num_agents_to_assign = math.ceil(homogeneity_probability * num_agent)
#     if num_agents_to_assign < 1:
#         num_agents_to_assign = 1
#
#     agent_index = 0  # 每次从上次结束的后一个开始
#     for cls_index in range(num_cls_index_ls):
#         agents_actions[agent_index].append(cls_index)
#         agent_index = (agent_index + 1) % num_agent
#
#     # 剩下的随机分配
#     num_agents_to_assign -= 1
#     # 将动作分配给这些智能体
#     for cls_index in range(num_cls_index_ls):
#         assigned_agents = random.sample(range(num_agent), num_agents_to_assign)
#         for agent_index in assigned_agents:
#             agents_actions[agent_index].append(cls_index)
#
#     return agents_actions


# 完全随机分配
# def generate_agents_actions(num_cls_index_ls, num_agent, homogeneity_probability):
#     agents_actions = [[] for _ in range(num_agent)]
#
#     # 计算需要分配给的智能体数量
#     num_agents_to_assign = math.ceil(homogeneity_probability * num_agent)
#     if num_agents_to_assign < 1:
#         num_agents_to_assign = 1
#
#     for cls_index in range(num_cls_index_ls):
#         assigned_agents = random.sample(range(num_agent), num_agents_to_assign)
#         for agent_index in assigned_agents:
#             agents_actions[agent_index].append(cls_index)
#
#     return agents_actions

# 完全异构 无论何时 都要保证每个机器人至少有一个动作
def generate_agents_actions(num_cls_index_ls, num_agent, homogeneity_probability):
    agents_actions = [[] for _ in range(num_agent)]

    # 计算需要分配给的智能体数量
    num_agents_to_assign = math.ceil(homogeneity_probability * num_agent)
    if num_agents_to_assign < 1:
        num_agents_to_assign = 1

    num_cls_to_assign_remain =  [num_agents_to_assign for _ in range(num_cls_index_ls)]
    agents_ls_of_cls_already_assign = [[] for _ in range(num_cls_index_ls)]

    # 确保每个机器人至少分配到一个动作
    # 初始化一个从0到num_cls_index_ls-1的列表
    available_indices = list(range(num_cls_index_ls))
    for agent_index in range(num_agent):
        if available_indices:
            # 随机选择一个可用的索引
            chosen_index = random.choice(available_indices)
            # 添加到对应的 agent 的行动列表
            agents_actions[agent_index].append(chosen_index)
            # 从可用列表中移除这个索引
            available_indices.remove(chosen_index)

            num_cls_to_assign_remain[chosen_index] -= 1
            agents_ls_of_cls_already_assign[chosen_index].append(agent_index)



    # 分配剩余的动作
    for cls_index in range(num_cls_index_ls):
        # assigned_agents = random.sample(set[range(num_agent)]-set(agents_ls_of_cls_already_assign[chosen_index]), num_cls_to_assign_remain[cls_index])

        # Convert both the total agents and the already assigned agents to sets
        total_agents = set(range(num_agent))
        already_assigned_agents = set(agents_ls_of_cls_already_assign[cls_index])

        # Perform set difference to get the list of agents not already assigned
        available_agents = list(total_agents - already_assigned_agents)
        # print("already_assigned_agents:",already_assigned_agents, "available_agents:",available_agents,num_cls_to_assign_remain[cls_index])
        assigned_agents = random.sample(available_agents, num_cls_to_assign_remain[cls_index])

        for agent_index in assigned_agents:
            agents_actions[agent_index].append(cls_index)

    return agents_actions


def assign_action_cls_to_agents():
    behavior_lib_path = f"{root_path}/envs/gridenv/minigrid_computation_env/behavior_lib"
    behavior_lib = BehaviorLibrary(behavior_lib_path)
    cls_ls = []
    for action_cls_name in ["OpenRoom","MovePackage"]:
        for room_id in range(num_rooms):
            pkg_id = room_id
            cls = type(f"{action_cls_name}_{pkg_id}", (behavior_lib["Action"][action_cls_name],), {})
            if action_cls_name=="OpenRoom":
                cls.room_id = pkg_id
            elif action_cls_name=="MovePackage":
                cls.pkg_id = pkg_id
            cls_ls.append(cls)

    agent_action_index_ls = generate_agents_actions(len(cls_ls), num_agent, homogeneity_probability)
    print("agent_action_index_ls:",agent_action_index_ls)

    for i, agent in enumerate(env.agents):

        action_ls = []
        for cls_index in agent_action_index_ls[i]:
            action_ls.append(cls_ls[cls_index])

        agent.behavior_dict = {
            "Action": action_ls,
            "Condition": behavior_lib["Condition"].values()
        }
        agent.create_behavior_lib()


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



num_agent = 4
num_rooms = 4
# num_objs = 2
action_fail_p = 0
bt_draw = False

if num_agent == 8:
    homogeneity_probability_ls = [i / 8 for i in range(1, 9)]
else:
    homogeneity_probability_ls = [0.25, 0.5, 0.75, 1]
homogeneity_probability = 1
use_subtask_chain = True

# 创建一个空的字典用于存储数据
data = {'homogeneity_probability': homogeneity_probability_ls}

for use_subtask_chain in [True,False]:
    col_name = f'use_subtask_chain={use_subtask_chain}'
    data[col_name] = []
    for homogeneity_probability in homogeneity_probability_ls:

        print_colored(
            f"============= use_subtask_chain:{use_subtask_chain} =========== homogeneity_probability: {homogeneity_probability} ========================",
            "purple")

        # 随机生成物品和物品所在的房间
        goal =  set()
        start = set()
        start_objects_rooms_dic = {}
        target_room_ls = list(range(num_rooms-1,-1,-1))
        # random.shuffle(target_room_ls)
        for pkg_id,room_id in enumerate(target_room_ls):
            goal.add(f"IsInRoom(package-{pkg_id},room-{room_id})")
            start.add(f"IsInRoom(package-{pkg_id},room-{pkg_id})")
            start.add(f"IsClose(room-{pkg_id})")
            start_objects_rooms_dic[pkg_id] = pkg_id
        goal = frozenset(goal)
        start = frozenset(start)


        # 初始环境
        env = MiniCompEnv(num_agent=num_agent,goal=goal,start=start)
        env.num_rooms = num_rooms
        env.target_room_ls = target_room_ls
        # env.num_objs = num_objs
        env.objects_rooms_dic = start_objects_rooms_dic
        env.use_atom_subtask_chain = use_subtask_chain
        env.action_fail_p = action_fail_p




        success_time = 0
        total_env_step_ls = []
        total_time = 500
        for time_id in range(total_time):
            print_colored(f"==================================== time_id: {time_id} ==============================================",
                          "green")
            if time_id == 9:
                xx=1

            # #########################
            # 随机分配动作
            # #########################
            assign_action_cls_to_agents()
            agent_actions_model = env.create_action_model()
            for i, actions in enumerate(agent_actions_model):
                print(f"Agent {i + 1} actions:")
                for action in actions:
                    print(f"  act:{action.name} pre:{action.pre} add:{action.add} del:{action.del_set}")


            # #########################
            # Run Decentralized multi-agent BT algorithm
            # #########################
            print_colored(f"Start Multi-Robot Behavior Tree Planning...",color="green")
            start_time = time.time()

            # start = None
            # planning_algorithm = MAOBTP(verbose = False,start=start,env=env)
            # # planning_algorithm.planning(frozenset(goal),action_lists=action_model)
            # planning_algorithm.bfs_planning(frozenset(goal),action_lists=action_lists)
            # behavior_lib = [agent.behavior_lib for agent in env.agents]
            # btml_list = planning_algorithm.get_btml_list()


            from mabtpg.btp.mabtp import MABTP
            planning_algorithm = MABTP(verbose = False,start=start)
            planning_algorithm.planning(frozenset(goal),action_lists=agent_actions_model)

            print_colored(f"Finish Multi-Robot Behavior Tree Planning!",color="green")
            print_colored(f"Time: {time.time()-start_time}",color="green")


            # Convert to BT and bind the BT to the agent
            behavior_lib = [agent.behavior_lib for agent in env.agents]
            bt_list = planning_algorithm.output_bt_list(behavior_libs=behavior_lib)
            # pruned_bt_list = planning_algorithm.new_output_pruned_bt_list(behavior_libs=behavior_lib)
            bind_bt(bt_list)


            # #########################
            # Simulation
            # #########################
            print_colored(f"start: {start}", "blue")
            env.print_ticks = bt_draw
            env.verbose = bt_draw
            env.reset()
            done = False
            max_env_step = 20
            env_steps = 0
            new_env_step = 0
            agents_steps = 0
            obs = set(start)
            env.state = obs
            while not done:
                obs, done, _, _, agents_one_step,finish_and_fail = env.step()
                env_steps += 1
                agents_steps += agents_one_step
                # if env_steps%50==0:
                print_colored(f"========= env_steps: {env_steps} ===============",
                          "blue")
                print_colored(f"state: {obs}", "blue")
                if obs >= goal:
                    done = True
                    break
                if finish_and_fail:
                    done=False
                    break
                if env_steps >= max_env_step:
                    break
            print(f"\ntask finished!")
            print_colored(f"goal:{goal}", "blue")
            print("obs>=goal:", obs >= goal)
            if obs >= goal:
                success_time +=1
                done = True
            else:
                sys.exit()
            total_env_step_ls.append(env_steps)
            print("env_steps:",env_steps)

        print(f"success rate:{success_time/total_time*100} %")
        print(f"Avg env_step:{sum(total_env_step_ls) / len(total_env_step_ls)}")
        avg_env_step = sum(total_env_step_ls) / len(total_env_step_ls)


        data[col_name].append(avg_env_step)

# 创建数据框
df = pd.DataFrame(data)
df.set_index('homogeneity_probability', inplace=True)

def print_summary_table(df, formatted=True):
    if formatted:
        print(df.to_string(index=True))
    else:
        print(df.to_csv(index=True, sep='\t'))
# Print the summary table in both formats
print("Formatted table:")
print_summary_table(df, formatted=True)

print("\nCSV formatted table:")
print_summary_table(df, formatted=False)