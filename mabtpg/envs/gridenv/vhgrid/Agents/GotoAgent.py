
from mabtpg.envs.gridenv.base.agent import Agent
from mabtpg.utils import get_root_path
from mabtpg.behavior_tree.behavior_library import BehaviorLibrary

from mabtpg.envs.gridenv.vhgrid.behavior_lib import *

# root_path = get_root_path()
# behavior_lib_path = f"{root_path}/envs/gridenv/vhgrid/behavior_lib"
# behavior_lib = BehaviorLibrary(behavior_lib_path)


class GotoAgent(Agent):
    behavior_dict = {
        "Action": [GoTo],
        "Condition": [IsNear]
    }
