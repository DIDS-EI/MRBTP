import time
import random
import math
import numpy as np
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
from mabtpg.envs.numerical_env.numsim_tools import create_directory_if_not_exists, print_action_data_table



behavior_lib_path = f"{root_path}/envs/gridenv/minigrid_computation_env/behavior_lib"
behavior_lib = BehaviorLibrary(behavior_lib_path)

random.seed(0)
np.random.seed(0)


def generate_agents_actions(index, num_agent, homogeneity_probability):
    agents_actions = [[] for _ in range(num_agent)]

    for cls_index in range(index):
        # 计算需要分配给的智能体数量
        num_agents_to_assign = math.ceil(homogeneity_probability * num_agent)
        if num_agents_to_assign<1:
            num_agents_to_assign = 1

        # 随机选择这些智能体
        assigned_agents = random.sample(range(num_agent), num_agents_to_assign)

        # 将动作分配给这些智能体
        for agent_index in assigned_agents:
            agents_actions[agent_index].append(cls_index)

    return agents_actions


def assign_action_cls_to_agents():
    room_cls_ls = []
    for room_id in range(num_rooms):
        room_cls = type(f"OpenRoom_{room_id}", (behavior_lib["Action"]["OpenRoom"],), {})
        room_cls.room_id = room_id
        room_cls_ls.append(room_cls)

    package_cls_ls = {}
    # for action_cls_name in ["PickUpInRoom","PutInRoom"]:
    for action_cls_name in ["MovePackage"]:
        package_cls_ls[action_cls_name] = []
        for pkg_id in range(num_rooms):
            pkg_cls = type(f"{action_cls_name}_{pkg_id}", (behavior_lib["Action"][action_cls_name],), {})
            pkg_cls.pkg_id = pkg_id
            package_cls_ls[action_cls_name].append(pkg_cls)

    rooms_cls_index = generate_agents_actions(num_rooms, num_agent, homogeneity_probability)
    package_cls_index = generate_agents_actions(num_rooms, num_agent, homogeneity_probability)

    for i, agent in enumerate(env.agents):
        action_ls = []
        for cls_index in rooms_cls_index[i]:
            action_ls.append(room_cls_ls[cls_index])
        for cls_index in package_cls_index[i]:
            # for action_cls_name in ["PickUpInRoom", "PutInRoom"]:
            for action_cls_name in ["MovePackage"]:
                action_ls.append(package_cls_ls[action_cls_name][cls_index])

        agent.behavior_dict = {
            "Action": action_ls,
            "Condition": behavior_lib["Condition"].values()
        }
        agent.create_behavior_lib()


def bind_bt():
    from mabtpg.behavior_tree.behavior_tree import BehaviorTree
    # new
    bt_list = []
    for i, agent in enumerate(planning_algorithm.planned_agent_list):
        bt = BehaviorTree(btml=btml_list[i], behavior_lib=behavior_lib[i])
        bt_list.append(bt)
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
homogeneity_probability = 1
use_subtask_chain = True
bt_draw = False

# 随机生成物品和物品所在的房间
goal =  set()
start = set()
start_objects_rooms_dic = {}
target_room_ls = list(range(num_rooms-1,-1,-1))
# random.shuffle(target_room_ls)
for pkg_id,room_id in enumerate(target_room_ls):
    goal.add(f"IsInRoom(package-{pkg_id},room-{room_id})")
    start.add(f"IsInRoom(package-{pkg_id},room-{pkg_id})")
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
planning_algorithm = MABTP(verbose = False,start=start,env=env)
planning_algorithm.planning(frozenset(goal),action_lists=agent_actions_model)
behavior_lib = [agent.behavior_lib for agent in env.agents]
btml_list = planning_algorithm.get_btml_list()

print_colored(f"Finish Multi-Robot Behavior Tree Planning!",color="green")
print_colored(f"Time: {time.time()-start_time}",color="green")



# 在规划出来的 BTML 里面加上 新的sub_btml_dict
bind_bt()


# #########################
# Simulation
# #########################
print_colored(f"start: {start}", "blue")
env.print_ticks = True
done = False
max_env_step = 500
env_steps = 0
new_env_step = 0
agents_steps = 0
obs = set(start)
env.state = obs
while not done:
    print_colored(f"==================================== {env_steps} ==============================================",
                  "blue")
    obs, done, _, _, agents_one_step = env.step()
    env_steps += 1
    agents_steps += agents_one_step
    print_colored(f"state: {obs}", "blue")
    if obs >= goal:
        done = True
        break
    if env_steps >= max_env_step:
        break
print(f"\ntask finished!")
print_colored(f"goal:{goal}", "blue")
print("obs>=goal:", obs >= goal)
if obs >= goal:
    done = True
