# from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.envs.gridenv.minigrid.behavior_lib.base.Action import MinigridAction as Action
from mabtpg.behavior_tree import Status
from minigrid.core.actions import Actions
from mabtpg.envs.gridenv.minigrid.objects import CAN_PICKUP,CAN_GOTO
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.envs.gridenv.minigrid.utils import get_direction_index
import random
from mabtpg.utils.astar import astar


class PutNearInRoom(Action):
    can_be_expanded = True
    num_args = 4
    valid_args = [CAN_PICKUP]

    def __init__(self, *args):
        super().__init__(*args)
        self.path = None
        self.source_obj_id = args[1]
        self.target_obj_id = args[2]
        self.room_index = int(args[3].split('-')[1])

        self.target_position = None
        self.target_obj_pos = None


    @classmethod
    def get_planning_action_list(cls, agent, env):

        room_num = len(env.room_cells)

        planning_action_list = []
        if "can_pickup" not in env.cache:
            env.cache["can_pickup"] = []
            env.cache["can_goto"] = []
            for obj in env.obj_list:
                if obj.type in cls.valid_args[0]:
                    env.cache["can_pickup"].append(obj.id)
                if obj.type in [CAN_GOTO]:
                    env.cache["can_goto"].append(obj.id)

        can_pickup = env.cache["can_pickup"]
        can_goto = env.cache["can_goto"]
        for obj_id in can_pickup:
            for target_obj_id in can_pickup:
                if obj_id == target_obj_id:
                    continue

                room_id = env.get_room_index(env.id2obj[target_obj_id].cur_pos)

                action_model = {}
                # error:if the agent go to in another room it will fail
                action_model["pre"]= {f"IsHolding(agent-{agent.id},{obj_id})",f"IsInRoom(agent-{agent.id},room-{room_id})"}

                action_model["add"]={f"IsHandEmpty(agent-{agent.id})",f"IsInRoom({obj_id},room-{room_id})",f"IsNear(agent-{agent.id},{obj_id})",f"CanGoTo({obj_id})"}
                action_model["add"]|={f"IsNear({obj_id},{target_obj_id})"}

                action_model["del_set"] = {f'IsHolding(agent-{agent.id},{obj.id})' for obj in env.obj_list}
                action_model["del_set"] |= {f'IsNear(agent-{agent.id},{obj})' for obj in can_goto if obj != obj_id}
                action_model["del_set"] |= {f'IsInRoom(agent-{agent.id},room-{rid})' for rid in range(room_num) if rid != room_id}
                # The dropped object can only live in one room: clear its presence in any other room.
                action_model["del_set"] |= {f'IsInRoom({obj_id},room-{rid})' for rid in range(room_num) if rid != room_id}
                # If we are dropping a key, we lose the right to open its door (frame symmetry of PickUp).
                if "key" in obj_id and obj_id in env.key_door_map:
                    door_id = env.key_door_map[obj_id]
                    action_model["del_set"] |= {f"CanOpen(agent-{agent.id},{door_id})"}
                action_model["cost"] = 1
                planning_action_list.append(PlanningAction(f"PutNearInRoom(agent-{agent.id},{obj_id},{target_obj_id},room-{room_id})",**action_model))

        return planning_action_list


    def update(self) -> Status:

        if self.check_if_pre_in_predict_condition():
            return Status.RUNNING

        if self.room_index not in self.env.room_cells.keys():
            raise ValueError(f"Room index {self.room_index} does not exist.")

        # Pick an empty cell adjacent to the target object as the drop position
        if self.target_position is None:
            target_obj = self.env.id2obj[self.target_obj_id]
            self.target_obj_pos = target_obj.cur_pos

            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(directions)

            for (dx, dy) in directions:
                nx, ny = self.target_obj_pos[0] + dx, self.target_obj_pos[1] + dy
                if (nx, ny) in self.env.room_cells[self.room_index]:
                    cell = self.env.minigrid_env.grid.get(nx, ny)
                    if cell is None:
                        self.target_position = (nx, ny)
                        break

        if self.target_position is None:
            return Status.FAILURE

        # Plan a path to the drop position
        if self.path is None:
            self.path = astar(self.env.grid, start=self.agent.position, goal=self.target_position)
            print(self.path)
            # astar may return None when other agents temporarily block the path
            if self.path is None:
                self.agent.action = Actions.done
                print("agent:", self.agent.id, " PutNearInRoom: no path, waiting")
                return Status.RUNNING

        # Reached the drop cell (or already standing on it): face it and drop
        if len(self.path) <= 1:
            if len(self.path) == 1:
                direction = self.path[0]
            else:
                # already on target_position, face the target object instead
                direction = (self.target_obj_pos[0] - self.agent.position[0],
                             self.target_obj_pos[1] - self.agent.position[1])
                if direction == (0, 0):
                    self.agent.action = Actions.done
                    return Status.RUNNING

            turn_to_action = self.turn_to(direction)
            if turn_to_action == Actions.done:
                # IMPORTANT: keep returning RUNNING here. If we returned
                # SUCCESS in the same tick, the parent Sequence would
                # advance to the next sibling immediately and that
                # sibling's update() would overwrite ``self.agent.action``
                # (set just below to ``drop``), so the ball would never
                # actually be dropped. Returning RUNNING lets the
                # simulator execute the drop action this tick; on the
                # next tick ``IsHolding`` becomes False and the BT
                # naturally moves on.
                self.agent.action = Actions.drop
                return Status.RUNNING
            self.agent.action = turn_to_action
            return Status.RUNNING

        # Walk along the planned path
        next_direction = self.path[0]
        turn_to_action = self.turn_to(next_direction)
        if turn_to_action == Actions.done:
            self.agent.action = Actions.forward
            self.path.pop(0)
        else:
            self.agent.action = turn_to_action
        print(self.path)
        print("agent:", self.agent.id, " PutNearInRoom:", self.source_obj_id, self.target_obj_id)
        return Status.RUNNING


    def turn_to(self,direction):
        direction_int = get_direction_index(direction)

        # Calculate the difference in direction
        diff = (direction_int - self.agent.direction) % 4

        # Determine the most natural turn action
        if diff == 1:
            return Actions.right
        elif diff == 3:
            return Actions.left
        elif diff == 2:
            # It might be either left or right, arbitrarily choose one
            return Actions.right
        else:
            return Actions.done # No turn needed if diff == 0