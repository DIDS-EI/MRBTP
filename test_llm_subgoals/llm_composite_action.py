from mabtpg.algo.llm_client.llms.gpt3 import LLMGPT3
import gymnasium as gym
from mabtpg import MiniGridToMAGridEnv
from minigrid.core.world_object import Ball, Box,Door
from mabtpg.utils import get_root_path
from mabtpg import BehaviorLibrary
root_path = get_root_path()
from itertools import permutations

from composite_action_tools import CompositeActionPlanner

num_agent = 2
env_id = "MiniGrid-DoorKey-16x16-v0"
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
env.reset(seed=0)

# add objs
ball = Ball('red')
env.place_object_in_room(ball,0)
# ball = Ball('yellow')
# env.place_object_in_room(ball,1)
env.reset(seed=0)


# goal = "IsNear(ball-0,ball-1)"
# goal = "IsInRoom(ball-0,room-1)"
action_lists = env.get_action_lists()
start = env.get_initial_state()
print(start)

action_sequences = {
    "GetKeyAndOpenDoor":['GoToInRoom', 'PickUp', 'GoToInRoom', 'Toggle'],
     "MoveItemBetweenRooms":['GoToInRoom', 'PickUp', 'GoBtwRoom', 'PutInRoom']
# "PickUpItemAndMove":['GoToInRoom', 'PickUp', 'GoToInRoom']
}

cap = CompositeActionPlanner(action_lists,action_sequences)
cap.get_composite_action()
comp_planning_act_dic = cap.comp_actions_dic
comp_act_BTML_dic = cap.comp_actions_BTML_dic


# set agent's planning agent
# for i in range(env.num_agent):
#     agent_id = "agent-"+str(i)
#     if agent_id in comp_planning_act_dic:
#         action_lists[i].extend(comp_planning_act_dic["agent-"+str(i)])
#     # sorted by cost
#     action_lists[i] = sorted(action_lists[i], key=lambda x: x.cost)


for i in range(env.num_agent):
    agent_id = "agent-"+str(i)
    action_lists[i]=[] # if only composition action
    if agent_id in comp_planning_act_dic:
        action_lists[i].extend(comp_planning_act_dic["agent-"+str(i)])
    # sorted by cost
    action_lists[i] = sorted(action_lists[i], key=lambda x: x.cost)


# 规划新的
from mabtpg.btp.maobtp import MAOBTP
goal = {"IsInRoom(ball-0,room-1)"}
# goal = {"IsOpen(door-0)"}
planning_algorithm = MAOBTP(verbose = False,start=start)
# planning_algorithm.planning(frozenset(goal),action_lists=action_lists)
planning_algorithm.bfs_planning(frozenset(goal),action_lists=action_lists)
behavior_lib = [agent.behavior_lib for agent in env.agents]
btml_list = planning_algorithm.get_btml_list()


# bt_list = planning_algorithm.output_bt_list([agent.behavior_lib for agent in env.agents])
# for i in range(env.num_agent):
#     print("\n" + "-" * 10 + f" Planned BT for agent {i} " + "-" * 10)
#     bt_list[i].save_btml(f"robot-{i}.bt")
#     bt_list[i].draw(file_name=f"agent-{i}")


# 在规划出来的 BTML 里面加上 新的sub_btml_dict
from mabtpg.behavior_tree.behavior_tree import BehaviorTree
from mabtpg.utils.any_tree_node import AnyTreeNode
from mabtpg.behavior_tree.constants import NODE_TYPE

# bt_list=[]
# for i,agent in enumerate(planning_algorithm.planned_agent_list):
#     for name,btml in comp_act_BTML_dic.items():
#         btml_list[i].anytree_root = agent.anytree_root
#         btml_list[i].sub_btml_dict[name] = btml
#         print("\n" + "-" * 10 + f" Planned BT for agent {i} " + "-" * 10)
#
#         tmp_bt = BehaviorTree(btml=btml, behavior_lib=behavior_lib[i])
#         tmp_bt.draw(file_name = name)
#
#     bt = BehaviorTree(btml=btml_list[i], behavior_lib=behavior_lib[i])
#     bt_list.append(bt)


# new
bt_list=[]
for i,agent in enumerate(planning_algorithm.planned_agent_list):
    for name,btml in comp_act_BTML_dic["agent-"+str(i)].items():
        btml_list[i].anytree_root = agent.anytree_root
        btml_list[i].sub_btml_dict[name] = btml
        print("\n" + "-" * 10 + f" Planned BT for agent {i} " + "-" * 10)

        tmp_bt = BehaviorTree(btml=btml, behavior_lib=behavior_lib[i])
        tmp_bt.draw(file_name = name)

    bt = BehaviorTree(btml=btml_list[i], behavior_lib=behavior_lib[i])
    bt_list.append(bt)





for i in range(env.num_agent):
    bt_list[i].save_btml(f"robot-{i}.bt")
    bt_list[i].draw(file_name=f"agent-{i}")

# bind the behavior tree to agents
for i,agent in enumerate(env.agents):
    agent.bind_bt(bt_list[i])


# run
env.render()
env.print_ticks = True
done = False
while not done:
    obs,done,_,_ = env.step()
print(f"\ntask finished!")

# continue rendering after task finished
while True:
    env.render()
