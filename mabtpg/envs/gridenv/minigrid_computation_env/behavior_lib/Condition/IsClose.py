from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status

import numpy as np
from minigrid.core.constants import DIR_TO_VEC
from mabtpg.envs.gridenv.minigrid_computation_env.base.WareHouseCondition import WareHouseCondition

class IsClose(WareHouseCondition):
    num_args = 1

    def __init__(self,*args):
        super().__init__(*args)

        self.room_id = self.args[0]




