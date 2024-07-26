from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status

import numpy as np


class NumCondition(Condition):

    def __init__(self,*args):
        super().__init__(*args)

    def update(self) -> Status:
        if self.name in self.env.state:
            return Status.SUCCESS
        else:
            return Status.FAILURE
