from mabtpg.algo.llm_client.llms.gpt3 import LLMGPT3
import gymnasium as gym
from mabtpg import MiniGridToMAGridEnv
from minigrid.core.world_object import Ball, Box,Door
from mabtpg.utils import get_root_path
from mabtpg import BehaviorTree, BehaviorLibrary
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
ball = Ball('green')
env.place_object_in_room(ball,0)
ball = Ball('yellow')
env.place_object_in_room(ball,1)
env.reset(seed=0)

goal = {"IsInRoom(ball-0,1)","IsInRoom(ball-1,1)"}
# goal = "IsNear(ball-0,ball-1)"


# 指定文件夹路径
behavior_lib_path = f"{root_path}/envs/gridenv/minigrid/behavior_lib"
behavior_lib = BehaviorLibrary(behavior_lib_path)
for cls in behavior_lib["Condition"].values():
    print(f"{cls.__name__}")
print("--------------")
for cls in behavior_lib["Action"].values():
    print(f"{cls.__name__}")
print("--------------")

# 首先得到环境地图
# print(env.minigrid_env.unwrapped)
map_str = env.get_map()
print(map_str)

# 输出环境中所有门的情况
for door,key in env.door_key_map.items():
    print(f"{door}: {key}")


# ============================================================
env.action_lists = env.get_action_lists()


# 输出并保存行为树
for i in range(env.num_agent):
    bt = BehaviorTree('subgoal.bt',behavior_lib=behavior_lib)
    env.agents[i].bind_bt(bt)



print('------- subgoal tree for agent-0  ---------')
env.agents[0].bt.print()
env.agents[0].bt.draw()

env.comm['subgoal_map'] = {
    'subgoal-0': frozenset({"IsOpen(door-0)"}),
    'subgoal-1': frozenset({"IsNear(ball-0,ball-2)"}),
    'subgoal-2': frozenset({"IsNear(ball-1,ball-2)"}),
}

env.comm['precondition'] = set()


# # When planning, directly remove this condition.
# subgoal =  subgoal_ls[1]
# # precondition = {"IsOpen(door-0)"}
# precondition= None
# planning_algorithm.planning(frozenset(subgoal),action_lists=action_lists ) #precondition=frozenset(precondition)
# bt_list = planning_algorithm.output_bt_list([agent.behavior_lib for agent in env.agents])
# subgoal_bt_ls[frozenset(subgoal)] = bt_list
#
#
# # bind the behavior tree to agents
# # 第一个智能体绑定完成第一个子目标的行为树
# env.agents[0].bind_bt(subgoal_bt_ls[frozenset(subgoal_ls[0])][0])
# # 第二个智能体绑定完成第二个子目标的行为树
# env.agents[1].bind_bt(subgoal_bt_ls[frozenset(subgoal_ls[1])][1])
#
#
# # 输出并保存行为树
# for i in range(env.num_agent):
#     print("\n" + "-" * 10 + f" Planned BT for agent {i} " + "-" * 10)
#     bt_list = subgoal_bt_ls[frozenset(subgoal_ls[0])] if i == 0 else subgoal_bt_ls[frozenset(subgoal_ls[1])]
#     bt_list[i].save_btml(f"robot-{i}.btml")
#     bt_list[i].draw(file_name=f"agent-{i}")


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

