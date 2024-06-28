from minigrid.core.actions import Actions
from mabtpg.behavior_tree.utils import Status

class Agent(object):
    def __init__(self,env=None,id=1):
        self.env = env
        self.id = id
        self.behavior_lib = None

        self.action = Actions.done
        self.bt_success = None

        self.pos = (-1, -1)
        self.dir = -1
        self.carrying = None

    def bind_bt(self,bt):
        self.bt = bt
        bt.bind_agent(self)

    def step(self):
        self.action = Actions.done
        self.bt.tick()
        self.bt_success = self.bt.root.status == Status.SUCCESS
        return self.action


class PickupAgent(Agent):
    pass