import gymnasium as gym
from mabtpg import MiniGridToMAGridEnv
from minigrid.core.world_object import Ball
from mabtpg.utils import get_root_path
from minigrid.core.world_object import Ball,Door,Key
root_path = get_root_path()
import random
import time
from mabtpg.utils.composite_action_tools import CompositeActionPlanner

from mabtpg.utils.tools import print_colored,filter_action_lists

from gymnasium.envs.registration import register
register(
    id="MiniGrid-KeyCorridorS3R1-v0-custom",
    entry_point="minigrid.envs:KeyCorridorEnv",
    kwargs={"room_size": 6, "num_rows": 2}, # 每个房间的格子总数，有几排房间
)


num_agent = 3
env_id = "MiniGrid-DoorKey-8x8-v0"
# env_id = "MiniGrid-RedBlueDoors-8x8-v0"
# env_id = "MiniGrid-KeyCorridorS3R1-v0-custom"
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
env.place_object_x_y(ball,4,5)
ball = Ball('green')
env.place_object_x_y(ball,3,2)

for obj in env.obj_list:
    if obj.type == "key":
        x,y = 1,5
        key = Key('yellow')
        env.put_obj(key,x,y)


# ball = Ball('green')
# env.place_object_in_room(ball,3)
# ball = Ball('purple')
# env.place_object_in_room(ball,4)

# key = Key('red')
# env.place_object_in_room(key,1)
# key = Key('green')
# env.place_object_in_room(key,1)
# key = Key('blue')
# env.place_object_in_room(key,1)
# key = Key('purple')
# env.place_object_in_room(key,1)
# ball = Ball('grey')
# env.place_object_in_room(ball,0)
# ball = Ball('red')
# env.place_object_in_room(ball,0)


# make the door open
# for obj in env.obj_list:
#     if obj.type == "door" and obj.color=="red":
#         x,y = obj.cur_pos[0],obj.cur_pos[1]
#         door = Door('red',is_open=True,is_locked=False)
#         env.put_obj(door,x,y)
#     if obj.type == "door" and obj.color!="red":
#         if random.random() < 0.3:
#             x,y = obj.cur_pos[0],obj.cur_pos[1]
#             door = Door('yellow',is_open=False,is_locked=True)
#             env.put_obj(door,x,y)
#         elif random.random() < 0.5:
#             x,y = obj.cur_pos[0],obj.cur_pos[1]
#             door = Door('green',is_open=False,is_locked=True)
#             env.put_obj(door,x,y)
        # elif random.random() < 0.8:
        #     x,y = obj.cur_pos[0],obj.cur_pos[1]
        #     door = Door('red',is_open=False,is_locked=False)
        #     env.put_obj(door,x,y)
        # elif random.random() < 0.9:
        #     x, y = obj.cur_pos[0], obj.cur_pos[1]
        #     door = Door('gray', is_open=False, is_locked=False)
        #     env.put_obj(door, x, y)

# make the door open
i=0
for obj in env.obj_list:
    if obj.type == "door":
        x,y = obj.cur_pos[0],obj.cur_pos[1]
        if i==0:
            obj.color = "yellow"
            i+=1
        door = Door(obj.color,is_open=False,is_locked=False)
        env.put_obj(door,x,y)

# door = Door('purple',is_open=False,is_locked=False)
# env.put_obj(door,5,8)

env.agents[1].pos = (5, 5)
env.agents[2].pos = (6, 6)

env.reset(seed=0)
while True:
    env.render()
