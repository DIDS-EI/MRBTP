from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status

import numpy as np


class NumCondition(Condition):

    def __init__(self,*args):
        super().__init__(*args)
        self.name = args[0]
        self.ins_name = self.modify_ins_name()


    def modify_ins_name(self):
        return f"{self.name}"

    def update(self) -> Status:
        if self.name in self.env.state:
            return Status.SUCCESS
        else:
            return Status.FAILURE
