from mabtpg.algo.llm_client.llms.gpt3 import LLMGPT3
import gymnasium as gym
from mabtpg import MiniGridToMAGridEnv
from minigrid.core.world_object import Ball, Box,Door
from mabtpg.utils import get_root_path
from mabtpg import BehaviorLibrary
root_path = get_root_path()





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
ball = Ball('yellow')
env.place_object_in_room(ball,1)
env.reset(seed=0)


goal = "IsNear(ball-0,ball-1)"


# 指定文件夹路径
behavior_lib_path = f"{root_path}/envs/gridenv/minigrid/behavior_lib"
behavior_lib = BehaviorLibrary(behavior_lib_path)
for cls in behavior_lib["Condition"].values():
    print(f"{cls.__name__}")
print("--------------")
for cls in behavior_lib["Action"].values():
    print(f"{cls.__name__}")

# 首先得到环境地图
# print(env.minigrid_env.unwrapped)
map_str = env.get_map()
print(map_str)

# 输出环境中所有门的情况
for door,key in env.door_key_map.items():
    print(f"{door}: {key}")



llm = LLMGPT3()

sub_act_ls = ['GoToInRoom', 'PickUp', 'GoToInRoom', 'Toggle']


from mabtpg.btp.sub_pbtp import SubPBTP

action_lists = action_lists + composite_action_lists

from mabtpg.btp.mabtp import MABTP

"robot1.btml"

from mabtpg.behavior_tree.btml.BTML import BTML
btml = BTML()

from mabtpg.utils.any_tree_node import AnyTreeNode
sequence_node = AnyTreeNode("sequence")
sequence_node.add_child(AnyTreeNode('Action', 'GoToInRoom', ('agent-0', 'key', 'room')))
sequence_node.add_child(AnyTreeNode('Action', 'PickUp', ('agent', 'key', 'room')))
sequence_node.add_child(AnyTreeNode('Action', 'GoToInRoom', ('agent', 'key', 'room')))
sequence_node.add_child(AnyTreeNode('Action', 'Toggle', ('agent', 'key', 'room')))

sub_btml = BTML()
sub_btml.cls_name = 'GetKeyAndOpenDoor'
sub_btml.var_args = ('agent-0','room-0','room-1')
sub_btml.anytree_root = sequence_node
btml.sub_btml_dict['GetKeyAndOpenDoor'] = sub_btml


