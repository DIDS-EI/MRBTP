from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status
from minigrid.core.actions import Actions
import random

class SelfDoTask(Action):
    can_be_expanded = False
    num_args = 1

    def __init__(self, *args):
        super().__init__(*args)

    def update(self) -> Status:
        self.agent.subtree.tick(verbose=True,bt_name=f' SelfDoTask {self.agent.agent_id}')

        return self.agent.subtree.root.status
