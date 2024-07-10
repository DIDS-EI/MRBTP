from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status

import numpy as np
from minigrid.core.constants import DIR_TO_VEC


class CanGoTo(Condition):
    '''Once an agent picks up an object, other agents cannot go to it anymore.'''
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

        #  For the door is locked and the agent has the corresponding key.
        self.obj = self.env.id2obj[self.obj_id]

        # Determine if `self.obj.cur_pos` is a numpy array and compare accordingly
        if isinstance(self.obj.cur_pos, np.ndarray):
            if (self.obj.cur_pos == (-1, -1)).all():
                return Status.FAILURE
        else:
            if self.obj.cur_pos == (-1, -1):
                return Status.FAILURE

        return Status.SUCCESS
