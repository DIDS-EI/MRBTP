from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status
from enum import IntEnum

import random


class Actions(IntEnum):
    # Turn left, turn right, move forward
    left = 0
    right = 1
    forward = 2
    # Pick up an object
    pickup = 3
    # Drop an object
    drop = 4
    # Toggle/activate an object
    toggle = 5

    # Done completing task
    done = 6


class RandomAction(Action):
    can_be_expanded = False
    num_args = 1

    def __init__(self, *args):
        super().__init__(*args)

    def update(self) -> Status:
        self.agent.actions = random.choice(list(Actions))
        print(f"randomly do action: {self.agent.actions.name}")
        return Status.RUNNING
