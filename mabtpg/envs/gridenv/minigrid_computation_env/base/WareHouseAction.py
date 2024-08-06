import random

from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status
from minigrid.core.actions import Actions
from mabtpg.envs.gridenv.minigrid.objects import CAN_TOGGLE
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.envs.gridenv.minigrid.utils import obj_to_planning_name, get_direction_index
import numpy as np
from mabtpg.utils.tools import print_colored,filter_action_lists
# random.seed(0)
# np.random.seed(0)

class WareHouseAction(Action):
    can_be_expanded = True
    num_args = 2
    valid_args = [CAN_TOGGLE]
    room_id = None

    def __init__(self, *args):
        super().__init__(*args)
        self.agent_id = args[0]
        self.pre = set()
        self.add = {f"IsOpen(room-{self.room_id})"}
        self.del_set = set()
        self.act_max_step = self.room_id

        self.act_cur_step = 0
        self.is_finish = False


    @classmethod
    def get_planning_action_list(cls, agent, env):
        planning_action_list = []

        action_model = {}
        # action_model["pre"] = {f"IsClose({obj_id})"}
        action_model["pre"] = set()
        action_model["add"]={f"IsOpen(room-{cls.room_id})"}
        action_model["del_set"] = set()
        action_model["cost"] = 1
        planning_action_list.append(PlanningAction(f"{cls.__name__}(agent-{agent.id})",**action_model))
        return planning_action_list


    def update(self) -> Status:

        if self.env.use_subtask_chain:
            if self.check_if_pre_in_predict_condition():
                return Status.RUNNING


        if self.agent.last_action==self:
            self.act_cur_step += 1
            if self.act_cur_step>=self.act_max_step:
                self.is_finish = True

                # execute
                if self.env.state >= self.pre:
                    if self.env.action_fail_p!=None and random.random()<self.env.action_fail_p:
                        print_colored(f"AGENT-{self.agent.id} {self.name} FAILURE!", color="red")
                        self.agent.is_fail = True
                        return Status.FAILURE
                    else:
                        self.env.state = (self.env.state | self.add) - self.del_set
                        self.env.agents_step += 1
                elif self.env.state < self.pre and self.is_finish:
                    print_colored(f"AGENT-{self.agent.id} cannot do it!", color="red")
                else:
                    print_colored(f"AGENT-{self.agent.id} is doing {self.name}", color="green")


        self.agent.action = self
        self.agent.last_action = self
        return Status.RUNNING