import gymnasium as gym
from mabtpg import MiniGridToMAGridEnv
from minigrid.core.world_object import Ball
from mabtpg.utils import get_root_path

root_path = get_root_path()
import time
from mabtpg.utils.composite_action_tools import CompositeActionPlanner

from mabtpg.utils.tools import print_colored,filter_action_lists

num_agent = 3
# env_id = "MiniGrid-DoorKey-8x8-v0"
register(
    id="MiniGrid-KeyCorridorS3R1-v0-custom",
    entry_point="minigrid.envs:KeyCorridorEnv",
    kwargs={"room_size": 3, "num_rows": 1}, # 每个房间的格子总数，有几排房间
)
env_id = "MiniGrid-KeyCorridorS3R1"
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
ball = Ball('purple')
env.place_object_in_room(ball,0)
ball = Ball('yellow')
env.place_object_in_room(ball,0)
# ball = Ball('grey')
# env.place_object_in_room(ball,0)
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

# goal = "IsNear(ball-0,ball-1)"
# goal = "IsInRoom(ball-0,room-1)"
action_lists = env.create_action_model()
start = env.get_initial_state()
print(start)

# action_sequences = {
#     # "GetObj": ['GoToInRoom', 'PickUp'],
#     # "ToggleDoor":['GoToInRoom','Toggle']
#     # "GetKeyAndOpenDoor":['GoToInRoom', 'PickUp', 'GoToInRoom', 'Toggle',"PutInRoom"],
#     # "PutDown":['']
#     # "PickUpItemAndMove":['GoToInRoom', 'PickUp', 'GoToInRoom']
#
#     # ['GoToInRoom', 'PickUp', 'GoToInRoom', 'Toggle','PutInRoom'], 怎么搜出来，现在的 CABTP 还是有问题。PutInRoom 后面规划不出 Toggle，不满足增加而不删除
#
#     "GetKeyAndOpenDoor":['GoToInRoom', 'PickUp', 'GoToInRoom', 'Toggle'],
#     # "PutObjInRoom":["PutInRoom"],
#      "MoveItemBetweenRooms":['GoToInRoom', 'PickUp', 'GoBtwRoom', 'PutInRoom'],
#     # "GoBtwRoom":["GoBtwRoom"]
#
#     # "GoAndPickUp": ['GoToInRoom', 'PickUp'],
#     # "GoToInRoom": ["GoToInRoom"],
#     # "Toggle": ["Toggle"],
#     # "MoveItemBetweenRooms": ['GoToInRoom', 'PickUp', 'GoBtwRoom', 'PutInRoom'],
# }

# agents_actions=[["GetKeyAndOpenDoor"],
#                 ["MoveItemBetweenRooms"]]

# agents_actions = [['GoToInRoom', 'PickUp', 'GoToInRoom', 'Toggle',],
#                   ['GoToInRoom', 'PickUp', 'GoBtwRoom', 'PutInRoom']]

# action_lists = filter_action_lists(action_lists,agents_actions)

# action_sequences = [
#     {
#         "GetKeyAndOpenDoor":['GoToInRoom(self,key-0,room-0)', 'PickUp(self,key-0)', 'GoToInRoom(self,door-0,room-0)', 'Toggle(self,door-0)'],
#         "Move0BetweenRooms": ['GoToInRoom(self,ball-0,room-0)', 'PickUp(self,ball-0)', 'GoBtwRoom(self,room-0,room-1)', 'PutInRoom(self,ball-0,room-1)'],
#         "Move1BetweenRooms": ['GoToInRoom(self,ball-1,room-0)', 'PickUp(self,ball-1)', 'GoBtwRoom(self,room-0,room-1)', 'PutInRoom(self,ball-1,room-1)'],
#     },
#     {
#         "GetKeyAndOpenDoor": ['GoToInRoom(self,key-0,room-0)', 'PickUp(self,key-0)', 'GoToInRoom(self,door-0,room-0)',
#                               'Toggle(self,door-0)'],
#         "Move0BetweenRooms": ['GoToInRoom(self,ball-0,room-0)', 'PickUp(self,ball-0)', 'GoBtwRoom(self,room-0,room-1)',
#                               'PutInRoom(self,ball-0,room-1)'],
#         "Move1BetweenRooms": ['GoToInRoom(self,ball-1,room-0)', 'PickUp(self,ball-1)', 'GoBtwRoom(self,room-0,room-1)',
#                               'PutInRoom(self,ball-1,room-1)'],
#     },
#     {
#         "GetKeyAndOpenDoor":['GoToInRoom(self,key-0,room-0)', 'PickUp(self,key-0)', 'GoToInRoom(self,door-0,room-0)', 'Toggle(self,door-0)'],
#         "Move0BetweenRooms": ['GoToInRoom(self,ball-0,room-0)', 'PickUp(self,ball-0)', 'GoBtwRoom(self,room-0,room-1)', 'PutInRoom(self,ball-0,room-1)'],
#         "Move1BetweenRooms": ['GoToInRoom(self,ball-1,room-0)', 'PickUp(self,ball-1)', 'GoBtwRoom(self,room-0,room-1)', 'PutInRoom(self,ball-1,room-1)'],
#     }
# ]

action_sequences = [
    {
        "GetKeyAndOpenDoor":['GoToInRoom(self,key-0,room-0)', 'PickUp(self,key-0)', 'GoToInRoom(self,door-0,room-0)', 'Toggle(self,door-0)'],
    },
    {
        "Move0BetweenRooms": ['GoToInRoom(self,ball-0,room-0)', 'PickUp(self,ball-0)', 'GoBtwRoom(self,room-0,room-1)',
                              'PutInRoom(self,ball-0,room-1)']
    },
    {
        "Move1BetweenRooms": ['GoToInRoom(self,ball-1,room-0)', 'PickUp(self,ball-1)', 'GoBtwRoom(self,room-0,room-1)', 'PutInRoom(self,ball-1,room-1)'],
    }
]

cap = CompositeActionPlanner(action_lists,action_sequences)
cap.get_composite_action()
comp_planning_act_dic = cap.planning_ls
comp_act_BTML_dic = cap.btml_ls


# set agent's planning agent
# for i in range(env.num_agent):
#     agent_id = "agent-"+str(i)
#     if agent_id in comp_planning_act_ls:
#         action_lists[i].extend(comp_planning_act_ls["agent-"+str(i)])
#     # sorted by cost
#     action_lists[i] = sorted(action_lists[i], key=lambda x: x.cost)


# for i in range(env.num_agent):
#     agent_id = "agent-"+str(i)
#     action_lists[i]=[] # if only composition action
#     if act_ls in comp_planning_act_dic:
#         action_lists[i].extend(comp_planning_act_ls["agent-"+str(i)])
#     # sorted by cost
#     action_lists[i] = sorted(action_lists[i], key=lambda x: x.cost)

for i in range(env.num_agent):
    # action_lists[i]=[]
    # action_lists[i].extend(comp_planning_act_dic[i])
    non_empty_acts = [act for act in comp_planning_act_dic[i] if act]
    action_lists[i].extend(non_empty_acts)
    action_lists[i] = sorted(action_lists[i], key=lambda x: x.cost)  # 不加也有问题？完全异构的第一个例子

# 规划新的
from mabtpg.btp.maobtp import MAOBTP
# goal = {"IsInRoom(ball-0,room-1)","IsInRoom(ball-1,room-1)","IsInRoom(ball-2,room-1)","IsInRoom(ball-3,room-1)","IsInRoom(ball-4,room-1)"}
# goal = frozenset({"IsInRoom(ball-0,room-1)","IsInRoom(ball-1,room-1)","IsInRoom(ball-2,room-1)"})
goal = frozenset({"IsInRoom(ball-0,room-1)","IsInRoom(ball-1,room-1)"})
# goal = {"IsNear(ball-0,door-0)"}
# goal = {"IsInRoom(ball-0,room-1)"}
# goal = {"IsInRoom(ball-0,room-1)"}
# goal = {"IsNear(ball-0,door-0)"}
# goal = {"IsOpen(door-0)"}

print_colored(f"Start Multi-Robot Behavior Tree Planning...",color="green")
start_time = time.time()
# start = None
planning_algorithm = MAOBTP(verbose = False,start=start,env=env)
# planning_algorithm.planning(frozenset(goal),action_lists=action_lists)
planning_algorithm.bfs_planning(frozenset(goal),action_lists=action_lists)
behavior_lib = [agent.behavior_lib for agent in env.agents]
btml_list = planning_algorithm.get_btml_list()


# from mabtpg.btp.mabtp import MABTP
# planning_algorithm = MABTP(verbose = False,start=start,env=env)
# planning_algorithm.planning(frozenset(goal),action_lists=action_lists)
# behavior_lib = [agent.behavior_lib for agent in env.agents]
# btml_list = planning_algorithm.get_btml_list()

print_colored(f"Finish Multi-Robot Behavior Tree Planning!",color="green")
print_colored(f"Time: {time.time()-start_time}",color="green")


# bt_list = planning_algorithm.output_bt_list([agent.behavior_lib for agent in env.agents])
# for i in range(env.num_agent):
#     print("\n" + "-" * 10 + f" Planned BT for agent {i} " + "-" * 10)
#     bt_list[i].save_btml(f"robot-{i}.bt")
#     bt_list[i].draw(file_name=f"agent-{i}")


# 在规划出来的 BTML 里面加上 新的sub_btml_dict
from mabtpg.behavior_tree.behavior_tree import BehaviorTree

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
for agent_id in range(num_agent):
    btml_list[agent_id].sub_btml_dict = comp_act_BTML_dic[agent_id].sub_btml_dict

    for name, sub_btml in btml_list[agent_id].sub_btml_dict.items():
        tmp_bt = BehaviorTree(btml=sub_btml, behavior_lib=behavior_lib[agent_id])
        tmp_bt.draw(file_name=f"data/{agent_id}-{name}")

bt_ls=[]
for i in range(num_agent):
    bt = BehaviorTree(btml=btml_list[i],behavior_lib=behavior_lib[i])
    bt_ls.append(bt)

    bt_ls[i].save_btml(f"robot-{i}.bt")
    bt_ls[i].draw(file_name=f"robot-{i}")

# bt_list=[]
# for agent_id,agent in enumerate(planning_algorithm.planned_agent_list):
#     btml_list[agent_id].sub_btml_dict = comp_act_BTML_dic[agent_id].sub_btml_dict
#
#     for name, sub_btml in comp_act_BTML_dic[agent_id].sub_btml_dict.items():
#         tmp_bt = BehaviorTree(btml=sub_btml, behavior_lib=behavior_lib[agent_id])
#         tmp_bt.draw(file_name=f"data/{agent_id}-{name}")

# bt_list=[]
# for i,agent in enumerate(planning_algorithm.planned_agent_list):
#     # for name,btml in comp_act_BTML_dic["agent-"+str(i)].items():
#     for j,(name, btml) in enumerate(comp_act_BTML_dic.items()):
#
#         btml_list[i].anytree_root = agent.anytree_root
#         btml_list[i].sub_btml_dict[name] = btml
#         print("\n" + "-" * 10 + f" Planned BT for agent {i} " + "-" * 10)
#
#         tmp_bt = BehaviorTree(btml=btml, behavior_lib=behavior_lib[i])
#         tmp_bt.draw(file_name = name+f"-{j}")
#
#     bt = BehaviorTree(btml=btml_list[i], behavior_lib=behavior_lib[i])
#     bt_list.append(bt)





# for i in range(env.num_agent):
#     bt_list[i].save_btml(f"robot-{i}.bt")
#     bt_list[i].draw(file_name=f"agent-{i}")
#
# # bind the behavior tree to agents
for i,agent in enumerate(env.agents):
    agent.bind_bt(bt_ls[i])


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
