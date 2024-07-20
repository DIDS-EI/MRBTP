from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status

class IsSelfTask(Condition):
    num_args = 1

    def __init__(self,subgoal):
        super().__init__(subgoal)
        self.subgoal = subgoal

    def update(self) -> Status:
        if self.subgoal == self.agent.accept_task:
            self.agent.current_task = self.subgoal
            return Status.SUCCESS
        else:
            return Status.FAILURE
