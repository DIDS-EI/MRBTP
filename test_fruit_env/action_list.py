from mabtpg import Random
Random.set_seed(0)

import gymnasium as gym


from mabtpg.envs.gridenv.vhgrid.fruit_env import FruitEnv
from mabtpg.envs.gridenv.vhgrid import Actions



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


action_list = [
    Actions.Forward(),
    Actions.Forward(),
    Actions.Forward(),
    Actions.PickUp("apple"),
    Actions.Turn(Actions.Turn.Direction.left),
    Actions.Forward(),
    Actions.Turn(Actions.Turn.Direction.right),
    Actions.PickUp("banana-0"),
    Actions.Turn(Actions.Turn.Direction.left),
    Actions.Forward(),
    Actions.Turn(Actions.Turn.Direction.right),
    Actions.PickUp(1),
    Actions.PutDown(),
    Actions.Turn(Actions.Turn.Direction.left),
    Actions.Forward(),
    Actions.Forward(),
    Actions.Forward(),
    Actions.Turn(Actions.Turn.Direction.right),
    Actions.PutDown("apple"),
    Actions.PutDown("apple"),
    Actions.PickUp("banana-0"),
    Actions.PickUp("banana"),
    Actions.Turn(Actions.Turn.Direction.right),
    Actions.Forward(),
    Actions.Forward(),
    Actions.Forward(),
    Actions.Forward(),
    Actions.Turn(Actions.Turn.Direction.left),
    Actions.PutDown(),
]



# 运行环境
env.reset()
env.render()
while True:
    if len(action_list)>0:
        actions = action_list.pop(0)
    else:
        actions = Actions.Idle()

    env.step(actions)

