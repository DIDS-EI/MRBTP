from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status

import numpy as np
from minigrid.core.constants import DIR_TO_VEC
from mabtpg.utils.astar import astar,is_near

# is agent near and facing to the target object
class IsNear(Condition):
    num_args = 2

    def __init__(self,*args):
        super().__init__(*args)

        self.target_agent = None

        self.target_obj_id = self.args[1]
        self.target_pos = None

        self.source_obj_id = self.args[0]
        self.source_pos = None

        self.obj_obj_flag = False




    def update(self) -> Status:

        other_do_it = self.check_if_in_predict_condition()
        if other_do_it:
            return Status.SUCCESS

        if "agent" not in self.args[0]:
            self.obj_obj_flag = True

        # agent and obj
        if self.obj_obj_flag == False:
            if self.target_agent is None:
                agent_id = int(self.args[0].split("-")[-1])
                self.target_agent = self.env.agents[agent_id]

            # Find the specific location of an object on the map based on its ID
            pos_str = self.env.id2obj[self.target_obj_id].cur_pos
            self.target_pos = list(pos_str)

            # pos_str = self.args[1].split("-")[-1]
            # self.target_pos = list(map(int, pos_str.split("_")))

            agent_facing_pos = self.target_agent.position + DIR_TO_VEC[self.target_agent.direction]
            if np.array_equal(self.target_pos, agent_facing_pos):
                return Status.SUCCESS
            else:
                return Status.FAILURE

        # obj and obj
        else:
            pos_str = self.env.id2obj[self.source_obj_id].cur_pos
            self.source_pos = list(pos_str)

            # Find the specific location of an object on the map based on its ID
            pos_str = self.env.id2obj[self.target_obj_id].cur_pos
            self.target_pos = list(pos_str)

            if is_near(self.source_pos,self.target_pos):
                return Status.SUCCESS
            else:
                return Status.FAILURE


