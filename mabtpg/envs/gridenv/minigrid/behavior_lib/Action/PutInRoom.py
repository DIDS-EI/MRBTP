# from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.envs.gridenv.minigrid.behavior_lib.base.Action import MinigridAction as Action
from mabtpg.behavior_tree import Status
from minigrid.core.actions import Actions
from mabtpg.envs.gridenv.minigrid.objects import CAN_PICKUP,CAN_GOTO
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.envs.gridenv.minigrid.utils import get_direction_index
from mabtpg.utils.astar import astar
import random


class PutInRoom(Action):
    can_be_expanded = True
    num_args = 3
    valid_args = [CAN_PICKUP]

    def __init__(self, *args):
        super().__init__(*args)
        self.path = None
        self.room_id = args[2] #int(''.join(filter(str.isdigit, args[2]))) #args[2]
        self.room_index = int(''.join(filter(str.isdigit, self.room_id )))
        self.target_position = None


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
        for room_id in range(room_num):
            for obj_id in can_pickup:
                action_model = {}
                # error:if the agent go to in another room it will fail
                action_model["pre"]= {f"IsHolding(agent-{agent.id},{obj_id})",f"IsInRoom(agent-{agent.id},room-{room_id})"}
                # action_model["pre"] = {f"IsHolding(agent-{agent.id},{obj_id})", f"IsInRoom({obj_id},{room_id})"}
                action_model["add"]={f"IsHandEmpty(agent-{agent.id})",f"IsInRoom({obj_id},room-{room_id})",f"IsNear(agent-{agent.id},{obj_id})",f"CanGoTo({obj_id})"}
                # action_model["del_set"] = {f"IsHolding(agent-{agent.id},{obj_id})"}
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
                planning_action_list.append(PlanningAction(f"PutInRoom(agent-{agent.id},{obj_id},room-{room_id})",**action_model))

        return planning_action_list


    def update(self) -> Status:

        if self.check_if_pre_in_predict_condition():
            return Status.RUNNING

        if self.room_index not in self.env.room_cells:
            raise ValueError(f"Room index {self.room_index} does not exist.")

        # Pick any empty cell inside the target room as the drop position.
        # We pick once and keep the choice across ticks (sticky), mirroring
        # ``PutNearInRoom``. Other agents are NOT stored in the grid, so
        # ``grid.get(x, y) is None`` is a true "empty cell" check; the path
        # planner will route around them implicitly.
        if self.target_position is None:
            agent_pos = tuple(int(c) for c in self.agent.position)
            room_cells = list(self.env.room_cells[self.room_index])
            random.shuffle(room_cells)
            for (cx, cy) in room_cells:
                if (cx, cy) == agent_pos:
                    # ``Actions.drop`` places the held object in front of
                    # the agent, not on its own cell, so we must stop one
                    # step short of the drop cell.
                    continue
                if self.env.minigrid_env.grid.get(cx, cy) is None:
                    self.target_position = (cx, cy)
                    self.path = None
                    break

        if self.target_position is None:
            return Status.FAILURE

        # Re-plan every tick from the agent's current position. This is
        # robust against the agent being nudged off the previously planned
        # path by a sibling subtree and is cheap on a 8x8 grid.
        self.path = astar(self.env.grid, start=self.agent.position, goal=self.target_position)
        if self.path is None:
            # Truly unreachable (e.g. closed door we can't open). Wait a
            # tick; the world might change.
            self.agent.action = Actions.done
            return Status.RUNNING

        # ``path == []`` -> agent is standing on the drop cell. Retarget on
        # the next tick (we cannot drop on our own cell).
        if len(self.path) == 0:
            self.target_position = None
            self.agent.action = Actions.done
            return Status.RUNNING

        # One step away from the drop cell: face it and drop. MiniGrid's
        # ``drop`` action places the held object on the cell in front of
        # the agent, so stopping one step short and facing the target puts
        # the object exactly there.
        if len(self.path) == 1:
            turn_to_action = self.turn_to(self.path[0])
            if turn_to_action == Actions.done:
                # Keep RUNNING so the parent Sequence does not advance and
                # overwrite ``agent.action`` before the simulator executes
                # the drop this tick.
                self.agent.action = Actions.drop
                return Status.RUNNING
            self.agent.action = turn_to_action
            return Status.RUNNING

        # Walk along the planned path.
        next_direction = self.path[0]
        turn_to_action = self.turn_to(next_direction)
        if turn_to_action == Actions.done:
            self.agent.action = Actions.forward
        else:
            self.agent.action = turn_to_action
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