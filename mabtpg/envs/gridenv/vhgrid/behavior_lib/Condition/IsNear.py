from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status

import numpy as np
from minigrid.core.constants import DIR_TO_VEC

# 在Minigrid环境中判断智能体是否与物体相邻且面对物体
class IsNear(Condition):
    num_args = 2

    def __init__(self,*args):
        ins_name = self.__class__.get_ins_name(*args)
        self.args = args
        self.agent = None
        self.env = None

        super().__init__(*args)

        self.target_agent = None
        self.target_pos = None




    def update(self) -> Status:
        if self.target_agent is None:
            agent_id = int(self.args[0].split("_")[-1])
            self.target_agent = self.env.agents[agent_id]
            pos_str = self.args[1].split("-")[-1]
            self.target_pos = list(map(int, pos_str.split("_")))

        agent_facing_pos = self.target_agent.pos + DIR_TO_VEC[self.target_agent.dir]
        if np.array_equal(self.target_pos, agent_facing_pos):
            return Status.SUCCESS
        else:
            return Status.FAILURE
