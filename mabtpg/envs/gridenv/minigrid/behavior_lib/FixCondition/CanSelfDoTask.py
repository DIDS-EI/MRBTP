from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status

class CanSelfDoTask(Condition):
    num_args = 1

    def update(self) -> Status:
        return Status.SUCCESS

