# from mabtpg.envs.virtualhome.base.vh_env import VHEnv
from mabtpg.envs.virtualhome.base.vh_env import VHEnv
from mabtpg.envs.base.env import Env

class VHEnvTest(VHEnv):
    agent_num = 1
    print_ticks = True

    def __init__(self):
        super().__init__()


    def reset(self):
        self.load_scenario(6) # 18



    def task_finished(self):
        if {"IsIn(milk,fridge)","IsClosed(fridge)"} <= self.agents[0].condition_set:
            return True
        else:
            return False
