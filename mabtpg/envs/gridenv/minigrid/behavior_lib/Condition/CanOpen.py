from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status

import numpy as np
from minigrid.core.constants import DIR_TO_VEC


class CanOpen(Condition):
    num_args = 2

    def __init__(self,*args):
        super().__init__(*args)

        self.target_agent = None
        self.obj_id = self.args[1]
        self.obj = None

    def update(self) -> Status:
        is_in_predict, is_true = self.check_if_in_predict_condition()
        if is_in_predict:
            if is_true:
                return Status.SUCCESS
            else:
                return Status.FAILURE

        if self.target_agent is None:
            agent_id = int(self.args[0].split("-")[-1])
            self.target_agent = self.env.agents[agent_id]

        #  For the door is locked and the agent has the corresponding key.
        self.obj = self.env.id2obj[self.obj_id]

        if self.obj.is_locked == True:
            if self.target_agent.carrying == None:
                return Status.FAILURE
            else:
                if self.target_agent.carrying.id != self.env.door_key_map[self.obj_id]:
                    return Status.FAILURE
                else:
                    return Status.SUCCESS
        else:
            # print("CanOpen", self.obj_id)
            return Status.SUCCESS
