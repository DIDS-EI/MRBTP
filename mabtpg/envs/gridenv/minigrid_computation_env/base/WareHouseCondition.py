from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status

import numpy as np
from minigrid.core.constants import DIR_TO_VEC


class WareHouseCondition(Condition):
    num_args = 1

    def __init__(self,*args):
        super().__init__(*args)

        self.room_id = self.args[0]


    def update(self) -> Status:


        is_in_predict, is_true = self.check_if_in_predict_condition()
        if is_in_predict:
            if is_true or (self.name in self.env.state):
                return Status.SUCCESS
            elif not is_true or (self.name not in self.env.state):
                return Status.FAILURE

        if self.name in self.env.state:
            return Status.SUCCESS
        else:
            return Status.FAILURE


