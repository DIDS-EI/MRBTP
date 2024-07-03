from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status

import numpy as np
from minigrid.core.constants import DIR_TO_VEC


class IsClose(Condition):
    num_args = 1

    def __init__(self,*args):
        ins_name = self.__class__.get_ins_name(*args)
        self.args = args
        self.agent = None
        self.env = None

        super().__init__(*args)


        self.obj_id = self.args[0]
        self.obj = None

    def update(self) -> Status:

        # door
        self.obj = self.env.id2obj[self.obj_id]

        if self.obj.is_open:
            return Status.FAILURE
        else:
            return Status.SUCCESS

