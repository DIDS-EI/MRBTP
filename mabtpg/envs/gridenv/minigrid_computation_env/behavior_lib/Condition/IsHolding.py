from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status

import numpy as np
from minigrid.core.constants import DIR_TO_VEC
from mabtpg.envs.gridenv.minigrid_computation_env.base.WareHouseCondition import WareHouseCondition


class IsHolding(WareHouseCondition):
    num_args = 1

    def __init__(self,*args):
        super().__init__(*args)
        self.agent = self.args[0]
        self.room_id = self.args[1]


    def update(self) -> Status:

        if self.env.use_subtask_chain:
            is_in_predict, is_true = self.check_if_in_predict_condition()
            if is_in_predict:
                if is_true:
                    return Status.SUCCESS
                else:
                    return Status.FAILURE
        else:
            if self.name in self.env.state:
                return Status.SUCCESS
            else:
                return Status.FAILURE

