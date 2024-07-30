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

    @property
    def print_name(self):
        return f'{self.print_name_prefix}{self.ins_name}'

    def update(self) -> Status:

        is_in_predict, is_true = self.check_if_in_predict_condition()
        if is_in_predict:
            if is_true:
                return Status.SUCCESS
            else:
                return Status.FAILURE

        if self.name in self.env.state:
            return Status.SUCCESS
        else:
            return Status.FAILURE
