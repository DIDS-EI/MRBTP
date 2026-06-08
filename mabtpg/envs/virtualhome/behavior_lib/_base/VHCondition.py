from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status
from mabtpg.envs.gridenv.minigrid_computation_env.base.WareHouseCondition import WareHouseCondition



class VHCondition(WareHouseCondition):
    can_be_expanded = True
    num_args = 1

