from mabtpg.behavior_tree.utils import Status
from mabtpg.behavior_tree.behavior_library import BehaviorLibrary


class Agent(object):
    behavior_dict = {
        "Action": [],
        "Condition": []
    }
    response_frequency = 1

    def __init__(self,env=None,id=0,behavior_lib=None):
        super().__init__()
        self.env = env
        self.id = id
        if behavior_lib:
            self.behavior_lib = behavior_lib
        else:
            self.create_behavior_lib()

        self.bt = None
        self.bt_success = None

        self.position = (-1, -1)
        self.direction = 3
        self.carrying = None

        self.condition_set = set()
        self.init_statistics()


    def init_statistics(self):
        self.step_num = 1
        self.next_response_time = self.response_frequency
        self.last_tick_output = None

    def create_behavior_lib(self):
        self.behavior_lib = BehaviorLibrary()
        self.behavior_lib.load_from_dict(self.behavior_dict)

    @property
    def agent_id(self):
        return f'agent-{self.id}'

    def bind_bt(self,bt):
        self.bt = bt
        bt.bind_agent(self)


    def step(self, action=None):
        self.action = None

        if action is None:
            if self.bt:
                self.bt.tick(verbose=True,bt_name=f'{self.agent_id} bt')
                self.bt_success = self.bt.root.status == Status.SUCCESS
        else:
            self.action = action
        return self.action

