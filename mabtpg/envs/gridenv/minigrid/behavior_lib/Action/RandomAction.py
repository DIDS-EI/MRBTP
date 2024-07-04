from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status
from minigrid.core.actions import Actions
import random

class RandomAction(Action):
    can_be_expanded = False
    num_args = 1

    def __init__(self, *args):
        super().__init__(*args)

    def update(self) -> Status:
        self.agent.actions = random.choice(list(Actions))
        print(f"randomly do action: {self.agent.actions.name}")
        return Status.RUNNING
