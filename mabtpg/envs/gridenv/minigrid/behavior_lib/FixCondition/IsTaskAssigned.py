from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status

class IsTaskAssigned(Condition):
    num_args = 1

    def __init__(self,subgoal):
        super().__init__(subgoal)
        self.subgoal = subgoal

    def update(self) -> Status:
        if self.subgoal in self.env.comm['task']:
            return Status.SUCCESS
        else:
            return Status.FAILURE
