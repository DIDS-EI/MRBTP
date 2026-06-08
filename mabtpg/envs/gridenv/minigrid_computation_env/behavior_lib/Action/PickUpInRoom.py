from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status
from minigrid.core.actions import Actions
from mabtpg.envs.gridenv.minigrid.objects import CAN_PICKUP
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.envs.gridenv.minigrid.utils import obj_to_planning_name, get_direction_index
import numpy as np



class PickUpInRoom(Action):
    can_be_expanded = False
    num_args = 2
    valid_args = [CAN_PICKUP]
    pkg_id = None

    def __init__(self, *args):
        super().__init__(*args)
        self.agent = args[0]
        self.room_id = args[1]


    @classmethod
    def get_planning_action_list(cls, agent, env):
        planning_action_list = []

        for room_id in range(env.num_rooms):
            action_model = {}

            action_model["pre"] = {f"IsOpen(room-{room_id})", f"IsInRoom(package-{cls.pkg_id},room-{room_id})"}
            action_model["add"] = {f"IsHolding(agent-{agent.id},package-{cls.pkg_id})"}
            action_model["del_set"] = {f"IsInRoom(package-{cls.pkg_id},room-{room_id})"}
            action_model["cost"] = 1
            planning_action_list.append(PlanningAction(f"{cls.__name__}(agent-{agent.id},room-{room_id})",**action_model))

        return planning_action_list


    def update(self) -> Status:

        if self.check_if_pre_in_predict_condition():
            return Status.RUNNING

        self.agent.action = Actions.pickup
        print("agent:", self.agent.id, " PickUp")
        return Status.RUNNING