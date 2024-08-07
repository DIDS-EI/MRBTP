from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status
from minigrid.core.actions import Actions
from mabtpg.envs.gridenv.minigrid.objects import CAN_PICKUP,CAN_GOTO
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.envs.gridenv.minigrid.utils import get_direction_index
import random


class PutInRoom(Action):
    can_be_expanded = False
    num_args = 3
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

            action_model["pre"] = {f"IsOpen(room-{room_id})", f"IsHolding(agent-{agent.id},package-{cls.pkg_id})"}
            action_model["add"] = {f"IsInRoom(package-{cls.pkg_id},room-{room_id})"}
            action_model["del_set"] = {f"IsHolding(agent-{agent.id},package-{cls.pkg_id})"}
            action_model["cost"] = 1
            planning_action_list.append(PlanningAction(f"{cls.__name__}(agent-{agent.id},room-{room_id})",**action_model))

        return planning_action_list


    def update(self) -> Status:

        if self.env.use_atom_subtask_chain:
            if self.check_if_pre_in_predict_condition():
                return Status.RUNNING


        return Status.RUNNING
