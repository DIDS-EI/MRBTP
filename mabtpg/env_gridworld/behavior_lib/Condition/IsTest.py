from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status

class IsTest(Condition):
    can_be_expanded = True
    num_args = 1

    def update(self) -> Status:
        return Status.SUCCESS

