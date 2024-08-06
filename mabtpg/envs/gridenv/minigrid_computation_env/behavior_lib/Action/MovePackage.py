from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status
from minigrid.core.actions import Actions
from mabtpg.envs.gridenv.minigrid.objects import CAN_PICKUP
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.envs.gridenv.minigrid.utils import obj_to_planning_name, get_direction_index
import numpy as np
from mabtpg.envs.gridenv.minigrid_computation_env.base.WareHouseAction import WareHouseAction



class MovePackage(WareHouseAction):
    can_be_expanded = True
    num_args = 2
    valid_args = [CAN_PICKUP]
    pkg_id = None

    def __init__(self, *args):
        super().__init__(*args)
        self.agent = args[0]
        self.from_room_id = args[1].split("-")[-1]
        self.to_room_id = args[2].split("-")[-1]

        self.act_cur_step = 0

        self.pre = {f"IsOpen(room-{self.from_room_id})", f"IsOpen(room-{self.to_room_id})", f"IsInRoom(package-{self.pkg_id},room-{self.from_room_id})"}
        self.add = {f"IsInRoom(package-{self.pkg_id},room-{self.to_room_id})"}
        self.del_set =  {f"IsInRoom(package-{self.pkg_id},room-{self.from_room_id})"}
        self.act_max_step = abs(int(self.from_room_id) - int(self.to_room_id))


    @classmethod
    def get_planning_action_list(cls, agent, env):
        planning_action_list = []

        from_room_id = cls.pkg_id
        to_room_id = env.target_room_ls[cls.pkg_id]

        action_model = {}

        action_model["pre"] = {f"IsOpen(room-{from_room_id})", f"IsOpen(room-{to_room_id})", f"IsInRoom(package-{cls.pkg_id},room-{from_room_id})"}
        action_model["add"] = {f"IsInRoom(package-{cls.pkg_id},room-{to_room_id})"}
        action_model["del_set"] = {f"IsInRoom(package-{cls.pkg_id},room-{from_room_id})"}
        action_model["cost"] = 1
        planning_action_list.append(PlanningAction(f"{cls.__name__}(agent-{agent.id},room-{from_room_id},room-{to_room_id})",**action_model))

        return planning_action_list
