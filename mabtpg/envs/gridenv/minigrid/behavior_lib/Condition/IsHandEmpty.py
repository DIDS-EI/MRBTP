from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status

import numpy as np
from minigrid.core.constants import DIR_TO_VEC


class IsHandEmpty(Condition):
    num_args = 1

    def __init__(self,*args):
        super().__init__(*args)

        self.target_agent = None


    def update(self) -> Status:
        if self.target_agent is None:
            agent_id = int(self.args[0].split("-")[-1])
            self.target_agent = self.env.agents[agent_id]

        if self.target_agent.carrying is None:
            return Status.SUCCESS
        else:
            return Status.FAILURE

