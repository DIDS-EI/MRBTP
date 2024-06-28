# from __future__ import annotations
import gymnasium as gym
from mabtpg import MiniGridToMAGridEnv
from mabtpg.env_gridworld.empty_env import EmptyEnv


num_agent = 3

tile_size = 32
agent_view_size =7
screen_size = 640

# MiniGrid
# env_id = "MiniGrid-Dynamic-Obstacles-16x16-v0" #"BabyAI-GoToLocalS8N7-v0"
# mingrid_env = gym.make(
#     env_id,
#     tile_size=tile_size,
#     render_mode=None,
#     agent_view_size=agent_view_size,
#     screen_size=screen_size
# )
# env = MiniGridToMAGridEnv(mingrid_env, num_agent=num_agent)

env_id = "MABTPG-Empty-16x16-v0"
env = EmptyEnv(tile_size, num_agent)
agents_start_pos = ((1, 1), (2, 1), (6, 6))
agents_start_dir = (0, 1, 2)
env = gym.make(
    env_id,
    num_agent=num_agent,
    agents_start_pos=agents_start_pos,
    agents_start_dir=agents_start_dir,

    tile_size=tile_size,
    render_mode="human",
    agent_view_size=agent_view_size,
    screen_size=screen_size
)


# BT规划算法，这里就直接加载随机行为树
from mabtpg import BehaviorTree, BehaviorLibrary

behavior_lib_path = f"../mabtpg/env_gridworld/minigrid/behavior_lib"
behavior_lib = BehaviorLibrary(behavior_lib_path)

print(behavior_lib)

# 绑定行为树
for agent in env.agents:
    bt = BehaviorTree("random.btml", behavior_lib)
    agent.bind_bt(bt)



# 运行环境
env.reset(seed=0)
env.render()
while True:
    env.step(None)

