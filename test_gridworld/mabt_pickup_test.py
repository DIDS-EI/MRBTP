import gymnasium as gym
from mabtpg import MiniGridToMAGridEnv


# main cfgs
num_agent = 2

# other cfgs
# env_id = "BabyAI-GoToObj-v0"  # goto
# env_id = "BabyAI-OneRoomS8-v0"  # goto pichup

env_id = "MiniGrid-DoorKey-16x16-v0"

# env_id = "BabyAI-GoToOpen-v0"
# env_id = "BabyAI-Open-v0"
# env_id = "BabyAI-BossLevel-v0"  # 4 conditions

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
    # goal = {"IsNear(agent-0,door-0)"}
    goal = {"IsOpen(door-0)"}  #需要有初始状态？IsClose

print("\n" + "-" * 10 + " get BT planning goal " + "-" * 10)
print("mission: " + env.mission)
print("BT goal: " + str(goal))

from mabtpg.mabtp.mabtp import MABTP

planning_algorithm = MABTP()
planning_algorithm.planning(frozenset(goal),action_lists=action_lists)
bt_list = planning_algorithm.output_bt_list([agent.behavior_lib for agent in env.agents])

for i in range(env.num_agent):
    print("\n" + "-" * 10 + f" Planned BT for agent {i} " + "-" * 10)
    bt_list[i].print()

# bind the behavior tree to agents
for i,agent in enumerate(env.agents):
    agent.bind_bt(bt_list[i])


# run env
env.render()
done = False
while not done:
    obs,done,_,_ = env.step()
print(f"\ntask finished!")

# continue rendering after task finished
while True:
    env.render()


