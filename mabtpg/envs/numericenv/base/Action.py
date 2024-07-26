from mabtpg.behavior_tree.base_nodes.BehaviorNode import BahaviorNode
from mabtpg.utils.tools import print_colored
from mabtpg.behavior_tree import Status
class NumAction(BahaviorNode):
    print_name_prefix = "action "
    type = 'Action'

    def __init__(self,action):
        self.name = action.name
        self.pre = action.pre
        self.add = action.add
        self.del_set = action.del_set
    @classmethod
    def get_info(self,*arg):
        return None

    def update(self) -> Status:
        self.agent.action = self.name
        self.env.state = (self.env.state | self.add) - self.del_set
        return Status.RUNNING


