
from gymnasium.envs.registration import register
from mabtpg.envs.gridenv.vhgrid.base.vhgrid_env import VHGridEnv

class FruitEnv(VHGridEnv):
    def __init__(self,**kwargs):
        self.num_agent = 3
        self.agents_start_pos = ((1, 1), (2, 1), (6, 6))
        self.agents_start_dir = (0, 1, 2)

        super().__init__(**kwargs)

        # self.agents = [PickupAgent(),GotoAgent()]


register(
    id="MABTPG-Fruit-v0",
    entry_point=__name__ + ":FruitEnv",
)
