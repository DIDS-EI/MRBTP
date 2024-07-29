from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status

import numpy as np
from minigrid.core.constants import DIR_TO_VEC


class IsOpen(Condition):
    num_args = 1

    def __init__(self,*args):
        super().__init__(*args)


        self.obj_id = self.args[0]
        self.obj = None


    def is_success(self):
        self.obj = self.env.id2obj[self.obj_id]

        return self.obj.is_open


    def update(self) -> Status:

        other_do_it = self.check_if_in_predict_condition()
        if other_do_it:
            return Status.SUCCESS

        return Status.SUCCESS if self.is_success() else Status.FAILURE
