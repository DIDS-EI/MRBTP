from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status

import numpy as np
from minigrid.core.constants import DIR_TO_VEC


# is agent near and facing to the target object
class IsInRoom(Condition):
    num_args = 2

    def __init__(self,*args):
        ins_name = self.__class__.get_ins_name(*args)
        self.args = args
        self.agent = None
        self.env = None

        super().__init__(*args)

        self.target_agent = None

        self.room_id = args[1]




    def update(self) -> Status:

        if self.target_agent is None:
            agent_id = int(self.args[0].split("-")[-1])
            self.target_agent = self.env.agents[agent_id]

        room_index = self.env.get_room_index(self.target_agent.position)
        if room_index == self.room_id:
            return Status.SUCCESS
        else:
            return Status.FAILURE
