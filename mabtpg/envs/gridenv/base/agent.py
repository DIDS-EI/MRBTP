from minigrid.core.actions import Actions
from mabtpg.behavior_tree.utils import Status
from mabtpg.behavior_tree.behavior_library import BehaviorLibrary

from mabtpg.envs.gridenv.base.Components import Container

class Agent(object):
    behavior_dict = {
        "Action": [],
        "Condition": []
    }

    def __init__(self,env=None,id=1,behavior_lib=None):
        self.env = env
        self.id = id
        if behavior_lib:
            self.behavior_lib = behavior_lib
        else:
            self.create_behavior_lib()

        self.action = Actions.done
        self.bt_success = None

        self.pos = (-1, -1)
        self.dir = -1
        self.carrying = False

        self.container = Container()

    def create_behavior_lib(self):
        self.behavior_lib = BehaviorLibrary()
        self.behavior_lib.load_from_dict(self.behavior_dict)



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