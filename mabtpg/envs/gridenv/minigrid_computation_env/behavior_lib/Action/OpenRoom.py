from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status
from minigrid.core.actions import Actions
from mabtpg.envs.gridenv.minigrid.objects import CAN_TOGGLE
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.envs.gridenv.minigrid.utils import obj_to_planning_name, get_direction_index
import numpy as np
from mabtpg.envs.gridenv.minigrid_computation_env.base.WareHouseAction import WareHouseAction



class OpenRoom(WareHouseAction):
    can_be_expanded = True
    num_args = 2
    valid_args = [CAN_TOGGLE]
    room_id = None

    def __init__(self, *args):
        super().__init__(*args)
        self.agent_id = args[0]
        self.pre = set()
        self.add = {f"IsOpen(room-{self.room_id})"}
        self.del_set = set()
        self.act_max_step = int(self.room_id)

        self.act_cur_step = 0


    @classmethod
    def get_planning_action_list(cls, agent, env):
        planning_action_list = []
        obj_id = f"room-{cls.room_id}"
        action_model = {}
        # action_model["pre"] = {f"IsClose({obj_id})"}
        action_model["pre"] = set()
        action_model["add"]={f"IsOpen({obj_id})"}
        action_model["del_set"] = set()
        action_model["cost"] = 1
        planning_action_list.append(PlanningAction(f"{cls.__name__}(agent-{agent.id})",**action_model))
        return planning_action_list

