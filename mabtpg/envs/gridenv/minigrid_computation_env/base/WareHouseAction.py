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


        if self.check_if_pre_in_predict_condition():
            return Status.RUNNING

        self.agent.current_task = {"task_id": self.name,
                                   "sub_goal": self.add,
                                   "sub_del": self.del_set}


        if self.agent.last_action and self.agent.last_action.name==self.name:
            self.agent.act_cur_step += 1
            if self.agent.act_cur_step>=self.act_max_step-1:
                self.is_finish = True

                # execute
                if self.env.state >= self.pre:
                    if self.env.action_fail_p!=None and random.random()<self.env.action_fail_p:
                        if self.env.verbose: print_colored(f"AGENT-{self.agent.id} {self.name} FAILURE!", color="red")
                        self.agent.is_fail = True
                        return Status.FAILURE
                    else:
                        self.env.state = (self.env.state | self.add) - self.del_set
                        self.env.agents_step += 1
                        print_colored(f"Auto Action {self.name} OK! state: {self.env.state}", "blue")
                elif self.env.state < self.pre and self.is_finish:
                    if self.env.verbose: print_colored(f"AGENT-{self.agent.id} cannot do it!", color="red")
                else:
                    if self.env.verbose: print_colored(f"AGENT-{self.agent.id} is doing {self.name}", color="green")
        else:
            self.agent.act_cur_step = 0

        self.agent.action = self
        self.agent.last_action = self
        return Status.RUNNING