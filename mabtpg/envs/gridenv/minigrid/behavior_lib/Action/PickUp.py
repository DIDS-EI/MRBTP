from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status
from minigrid.core.actions import Actions
from mabtpg.envs.gridenv.minigrid.objects import CAN_PICKUP
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.envs.gridenv.minigrid.utils import obj_to_planning_name, get_direction_index
import numpy as np



class PickUp(Action):
    num_args = 2
    valid_args = [CAN_PICKUP]

    def __init__(self, *args):
        super().__init__(*args)
        self.path = None

    @classmethod
    def get_planning_action_list(cls, agent, env):
        planning_action_list = []
        if "can_pickup" not in env.cache:
            env.cache["can_pickup"] = []
            for obj in env.obj_list:
                if obj.type in cls.valid_args[0]:
                    env.cache["can_pickup"].append(obj.id)
                    # env.cache["can_pickup"].append(obj_to_planning_name(obj))

        can_pickup = env.cache["can_pickup"]
        for obj_id in can_pickup:
            action_model = {}
            action_model["pre"]= {f"IsNear(agent-{agent.id},{obj_id})"}
            action_model["add"]={f"IsHolding(agent-{agent.id},{obj_id})"}
            action_model["del_set"] = set()
            action_model["cost"] = 1
            planning_action_list.append(PlanningAction(f"PickUp(agent-{agent.id},{obj_id})",**action_model))

        return planning_action_list


    def update(self) -> Status:

        self.agent.actions = Actions.pickup
        return Status.RUNNING