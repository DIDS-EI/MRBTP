import gymnasium as gym
from mabtpg import MiniGridToMAGridEnv
from minigrid.core.world_object import Ball, Box,Door

from gymnasium.envs.registration import register
# main cfgs
num_agent = 2


env_id = "MiniGrid-DoorKey-16x16-v0" #"MiniGrid-DoorKey-16x16-v0"


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

## ROOMS
# Output which positions each room contains
for room_index, cells in env.room_cells.items():
    print(f"Room {room_index}: {cells}")

# Query which room a specific position belongs to
room_index = env.get_room_index((1,2))
print("room_index:",room_index)

# Place an object in the room with the specified index
ball = Ball('red')
env.place_object_in_room(ball,0)
# ball = Ball('grey')
# env.place_object_in_room(ball,1)
# ball = Ball('yellow')
# env.place_object_in_room(ball,0)

# make the door open
# for obj in env.obj_list:
#     if obj.type == "door":
#         x,y = obj.cur_pos[0],obj.cur_pos[1]
#         door = Door('yellow',is_open=True,is_locked=False)
#         env.put_obj(door,x,y)


mission_str = env.mission
before_str = ", then "
after_str = " after you "

# split before/after
if before_str in mission_str:
    mission_list1 = mission_str.split(before_str)
elif after_str in mission_str:
    mission_list1 = mission_str.split(after_str)
else:
    mission_list1 = [mission_str]

and_str = " and "
# split and
mission_list = []
for mission_str in mission_list1:
    if and_str in mission_str:
        mission_list += mission_str.split(and_str)
    else:
        mission_list += [mission_str]



action_lists = env.get_action_lists()

goal = env.get_goal()
# 获取球的颜色和位置
if goal==None:
    # goal = {"IsHolding(agent-0,key-0)"}
    # goal = {"IsOpen(door-0)"}
    # goal = {"IsNear(agent-0,key-0)","IsNear(agent-1,key-0)"}
    # goal = {"IsInRoom(agent-0,1)"}
    # goal = {"IsInRoom(agent-0,1)", "IsInRoom(agent-1,1)"} # ???

    # goal = {"IsHolding(agent-0,ball-0)"}
    goal = {"IsInRoom(ball-0,1)"}
    # goal = {"IsInRoom(ball-0,0)","IsInRoom(ball-1,0)"}

    # goal = {"IsInRoom(ball-0,0)", "IsNear(agent-0,ball-2)","IsNear(agent-1,ball-2)"}



print("\n" + "-" * 10 + " get BT planning goal " + "-" * 10)
print("mission: " + env.mission)
print("BT goal: " + str(goal))

from mabtpg.mabtp.mabtp import MABTP

planning_algorithm = MABTP(verbose = False)
planning_algorithm.planning(frozenset(goal),action_lists=action_lists)
bt_list = planning_algorithm.output_bt_list([agent.behavior_lib for agent in env.agents])

for i in range(env.num_agent):
    print("\n" + "-" * 10 + f" Planned BT for agent {i} " + "-" * 10)
    bt_list[i].save_btml(f"robot-{i}.btml")

    bt_list[i].draw(file_name=f"agent-{i}")

# bind the behavior tree to agents
for i,agent in enumerate(env.agents):
    agent.bind_bt(bt_list[i])


# run env
env.render()
env.print_ticks = True
done = False
while not done:
    obs,done,_,_ = env.step()
print(f"\ntask finished!")

# continue rendering after task finished
while True:
    env.render()


