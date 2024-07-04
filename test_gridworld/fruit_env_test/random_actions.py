from mabtpg import Random
Random.set_seed(0)

import gymnasium as gym


from mabtpg.envs.gridenv.vhgrid.fruit_env import FruitEnv




#其他场景参数
env_id = "MABTPG-Fruit-v0"
tile_size = 32
agent_view_size =7
screen_size = 640

env = gym.make(
    env_id,
    tile_size=tile_size,
    render_mode="human",
    agent_view_size=agent_view_size,
    screen_size=screen_size
)


# BT规划算法，这里就直接加载随机行为树
from mabtpg import BehaviorTree, BehaviorLibrary

behavior_lib_path = f"../../mabtpg/envs/gridenv/vhgrid/behavior_lib"
behavior_lib = BehaviorLibrary(behavior_lib_path)
print(behavior_lib)

# 绑定行为树
for agent in env.agents:
    bt = BehaviorTree("random.btml", behavior_lib)
    agent.bind_bt(bt)



# 运行环境
env.reset()
env.render()
while True:
    env.step(None)

