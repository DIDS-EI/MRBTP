import copy

from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status
from minigrid.core.actions import Actions
import random

class SelfAcceptTask(Action):
    can_be_expanded = False
    num_args = 1

    def __init__(self, subgoal):
        super().__init__(subgoal)
        self.subgoal = subgoal

    def update(self) -> Status:

        # 是否有人做了，如果没人做我就做
        if self.subgoal not in self.env.blackboard["predict_condition"]:
            self.agent.accept_task = self.subgoal
            self.env.blackboard["predict_condition"] |= self.subgoal

        # self.env.blackboard['task'][self.subgoal] = self.agent.agent_id
        #
        # subgoal_set = self.env.blackboard['subgoal_map'][self.subgoal]
        #
        # self.agent.planning_for_subgoal(self.subgoal)
        #
        # self.env.blackboard['precondition'].update(subgoal_set)
        # self.agent.subgoal = self.subgoal

        return Status.RUNNING
