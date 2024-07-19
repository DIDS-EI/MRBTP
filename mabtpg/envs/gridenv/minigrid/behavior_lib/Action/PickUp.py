from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status
from minigrid.core.actions import Actions
from mabtpg.envs.gridenv.minigrid.objects import CAN_PICKUP
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.envs.gridenv.minigrid.utils import obj_to_planning_name, get_direction_index
import numpy as np



class PickUp(Action):
    can_be_expanded = True
    num_args = 2
    valid_args = [CAN_PICKUP]

    def __init__(self, *args):
        super().__init__(*args)
        self.path = None

    @classmethod
    def get_planning_action_list(cls, agent, env):
        planning_action_list = []
        room_num = len(env.room_cells)
        can_pickup = env.cache["can_pickup"]
        for obj_id in can_pickup:
            action_model = {}

            room_index = env.get_room_index(env.id2obj[obj_id].cur_pos)
            action_model["pre"]= {f"IsNear(agent-{agent.id},{obj_id})",f"IsHandEmpty(agent-{agent.id})",f"IsInRoom(agent-{agent.id},room-{room_index})"}
            action_model["add"]={f"IsHolding(agent-{agent.id},{obj_id})"}

            # get key that open one door
            if "key" in obj_id and obj_id in env.key_door_map:
                door_id = env.key_door_map[obj_id]
                action_model["add"] |= {f"CanOpen(agent-{agent.id},{door_id})"} # |

            action_model["del_set"] = {f"IsHandEmpty(agent-{agent.id})",f"CanGoTo({obj_id})",f"IsNear(agent-{agent.id},{obj_id})"}
            action_model["del_set"] = {f'IsInRoom(agent-{agent.id},room-{rid})' for rid in range(room_num) if rid != room_index}
            # delete all obj in hand
            action_model["del_set"] = {f'IsHolding(agent-{agent.id},{obj.id})' for obj in env.obj_list if obj.id != obj_id}

            action_model["del_set"] = {f'IsNear({obj_id},{obj.id})' for obj in env.obj_list if
                                       obj.id != obj_id}
            action_model["del_set"] = {f'CanGoTo({obj_id})' }


            action_model["cost"] = 1
            planning_action_list.append(PlanningAction(f"PickUp(agent-{agent.id},{obj_id})",**action_model))

        return planning_action_list


    def update(self) -> Status:

        self.agent.action = Actions.pickup
        return Status.RUNNING