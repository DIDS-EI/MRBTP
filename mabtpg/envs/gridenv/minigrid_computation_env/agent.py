from mabtpg.behavior_tree.utils import Status
from mabtpg.behavior_tree.behavior_library import BehaviorLibrary
import copy
from mabtpg.utils.tools import print_colored
from mabtpg.envs.numerical_env.agent import Agent as NumAgent

class Agent(NumAgent):
    def __init__(self,env=None,id=0,behavior_lib=None):
        super().__init__(env,id,behavior_lib)

        self.behavior_dict = {
            "Action": [],
            "Condition": []
        }

        self.is_fail = False


    def create_behavior_lib(self):
        self.behavior_lib = BehaviorLibrary()
        self.behavior_lib.load_from_dict(self.behavior_dict)
