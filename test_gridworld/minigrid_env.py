from __future__ import annotations
import gymnasium as gym
from mabtpg import MiniGridToMAGridEnv


#主要场景参数
num_agent = 3

#其他场景参数
env_id = "BabyAI-GoToLocalS8N7-v0"
tile_size = 32
agent_view_size =7
screen_size = 640

mingrid_env = gym.make(
    env_id,
    tile_size=tile_size,
    render_mode=None,
    agent_view_size=agent_view_size,
    screen_size=screen_size
)

env = MiniGridToMAGridEnv(mingrid_env, num_agent=num_agent)

# BT规划算法，这里就直接加载随机行为树
from mabtpg import BehaviorTree, BehaviorLibrary

behavior_lib_path = f"../mabtpg/env_gridworld/behavior_lib"
behavior_lib = BehaviorLibrary(behavior_lib_path)


# 绑定行为树
for agent in env.agents:
    bt = BehaviorTree("random.btml", behavior_lib)
    agent.bind_bt(bt)



# 运行环境
env.reset(seed=0)
env.render()
while True:
    env.step(None)

