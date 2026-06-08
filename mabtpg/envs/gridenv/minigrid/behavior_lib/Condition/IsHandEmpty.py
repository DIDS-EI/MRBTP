from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status

import numpy as np
from minigrid.core.constants import DIR_TO_VEC


class IsHandEmpty(Condition):
    num_args = 1

    def __init__(self,*args):
        super().__init__(*args)

        self.target_agent = None
        self.agent_id = None


    def update(self) -> Status:

        is_in_predict, is_true = self.check_if_in_predict_condition()
        if is_in_predict:
            if is_true:
                return Status.SUCCESS
            else:
                return Status.FAILURE

        if self.target_agent is None:
            self.agent_id = int(self.args[0].split("-")[-1])
            self.target_agent = self.env.agents[self.agent_id]

        if self.target_agent.carrying is None:
            # print("IsHandEmpty: ",self.agent_id)
            return Status.SUCCESS
        else:
            return Status.FAILURE

