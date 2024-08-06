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

random.seed(0)
np.random.seed(0)


def generate_agents_actions(total_actions_predicates, num_agent, homogeneity_probability):
    agents_actions = [[] for _ in range(num_agent)]

    for action in total_actions_predicates:
        # 计算需要分配给的智能体数量
        num_agents_to_assign = math.ceil(homogeneity_probability * num_agent)
        if num_agents_to_assign<1:
            num_agents_to_assign = 1

        # 随机选择这些智能体
        assigned_agents = random.sample(range(num_agent), num_agents_to_assign)

        # 将动作分配给这些智能体
        for agent_index in assigned_agents:
            agents_actions[agent_index].append(action)

    return agents_actions


num_agent = 3
env_id = "MiniGrid-DoorKey-16x16-v0"
# env_id = "MiniGrid-RedBlueDoors-8x8-v0"
tile_size = 32
agent_view_size =7
screen_size = 1024

mingrid_env = gym.make(
    env_id,
    tile_size=tile_size,
    render_mode=None,
    agent_view_size=agent_view_size,
    screen_size=screen_size
)


env = MiniGridToMAGridEnv(mingrid_env, num_agent=num_agent)
# env.reset(seed=0)

# add objs
ball = Ball('red')
env.place_object_in_room(ball,0)
ball = Ball('yellow')
env.place_object_in_room(ball,0)

# ball = Box('green')
# env.place_object_in_room(ball,1)

# key = Key('yellow')
# env.place_object_in_room(key,1)
# env.agents[1].pos = (8,8)

# ball = Ball('red')
# env.place_object_in_room(ball,0)
# ball = Ball('red')
# env.place_object_in_room(ball,0)
env.reset(seed=0)
# make the door open
# for obj in env.obj_list:
#     if obj.type == "door":
#         x,y = obj.cur_pos[0],obj.cur_pos[1]
#         door = Door('yellow',is_open=True,is_locked=False)
#         env.put_obj(door,x,y)


print("env.obj_list:",env.obj_list)


total_actions_model = env.create_action_model()
start = env.get_initial_state()
print(start)


total_actions_predicates = ['GoToInRoom','PickUp','Toggle',"PutInRoom",'PutNearInRoom','GoBtwRoom']



# agents_actions = [['GoToInRoom', 'PickUp', 'Toggle'],
#                   ['GoToInRoom', 'PickUp','GoBtwRoom', 'PutNearInRoom']]
homogeneity_probability = 1
agents_actions_predicates = generate_agents_actions(total_actions_predicates,num_agent,homogeneity_probability)
print("agents_actions_predicates:",agents_actions_predicates)
agent_actions_model = filter_action_lists(total_actions_model,agents_actions_predicates)

# agent_actions_model = total_actions_model

# 规划新的
from mabtpg.btp.maobtp import MAOBTP
# goal = {"IsNear(ball-0,box-0)","IsNear(ball-1,box-0)"}
goal = {"IsInRoom(ball-0,room-1)","IsInRoom(ball-1,room-1)"}
# goal = {"IsOpen(door-0)"}

print_colored(f"Start Multi-Robot Behavior Tree Planning...",color="green")
start_time = time.time()
# start = None
# planning_algorithm = MAOBTP(verbose = False,start=start,env=env)
# # planning_algorithm.planning(frozenset(goal),action_lists=agent_actions_model)
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
from mabtpg.behavior_tree.behavior_tree import BehaviorTree
# new
bt_list=[]
for i,agent in enumerate(planning_algorithm.planned_agent_list):
    bt = BehaviorTree(btml=btml_list[i], behavior_lib=behavior_lib[i])
    bt_list.append(bt)
for i in range(env.num_agent):
    bt_list[i].save_btml(f"robot-{i}.bt")
    # bt_list[i].draw(file_name=f"agent-{i}")
# bind the behavior tree to agents
for i,agent in enumerate(env.agents):
    agent.bind_bt(bt_list[i])


# run
env.render()
env.print_ticks = True
done = False
while not done:
    print_colored("======================================================================================","blue")
    obs,done,_,_ = env.step()
    # print("==========================\n")
print(f"\ntask finished!")

# continue rendering after task finished
while True:
    env.render()
