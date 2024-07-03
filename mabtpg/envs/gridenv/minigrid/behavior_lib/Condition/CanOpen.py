from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status

import numpy as np
from minigrid.core.constants import DIR_TO_VEC


class CanOpen(Condition):
    num_args = 1

    def __init__(self,*args):
        ins_name = self.__class__.get_ins_name(*args)
        self.args = args
        self.agent = None
        self.env = None

        super().__init__(*args)

        self.target_agent = None
        self.obj_id = self.args[1]
        self.obj = None

    def update(self) -> Status:
        if self.target_agent is None:
            agent_id = int(self.args[0].split("-")[-1])
            self.target_agent = self.env.agents[agent_id]

        #  For the door is locked and the agent has the corresponding key.
        self.obj = self.env.id2obj[self.obj_id]

        if self.obj.is_open == False and self.target_agent.carrying != self.env.door_key_map[self.obj_id]:
            return Status.FAILURE
        else:
            return Status.SUCCESS

