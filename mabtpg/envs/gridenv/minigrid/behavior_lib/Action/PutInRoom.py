from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status
from minigrid.core.actions import Actions
from mabtpg.envs.gridenv.minigrid.objects import CAN_PICKUP,CAN_GOTO
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.envs.gridenv.minigrid.utils import get_direction_index
import random


class PutInRoom(Action):
    can_be_expanded = True
    num_args = 3
    valid_args = [CAN_PICKUP]

    def __init__(self, *args):
        super().__init__(*args)
        self.path = None
        self.room_index = int(args[2])

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
                action_model["pre"]= {f"IsHolding(agent-{agent.id},{obj_id})",f"IsInRoom(agent-{agent.id},{room_id})"}
                # action_model["pre"] = {f"IsHolding(agent-{agent.id},{obj_id})", f"IsInRoom({obj_id},{room_id})"}
                action_model["add"]={f"IsHandEmpty(agent-{agent.id})",f"IsInRoom({obj_id},{room_id})",f"IsNear(agent-{agent.id},{obj_id})",f"CanGoTo({obj_id})"}
                action_model["del_set"] = {f"IsHolding(agent-{agent.id},{obj_id})"}
                action_model["del_set"] |= {f'IsNear(agent-{agent.id},{obj})' for obj in can_goto if obj != obj_id}
                action_model["del_set"] = {f'IsInRoom(agent-{agent.id},{rid})' for rid in range(room_num) if rid != room_id}
                action_model["cost"] = 1
                planning_action_list.append(PlanningAction(f"PutInRoom(agent-{agent.id},{obj_id},{room_id})",**action_model))

        return planning_action_list


    def update(self) -> Status:
        if self.room_index not in self.env.room_cells:
            raise ValueError(f"Room index {self.room_index} does not exist.")


        # first go to another room
        # if self.path is None:
        #     room_points_ls = self.env.room_cells[self.room_index]
        #     random.shuffle(room_points_ls)
        #     self.goal = room_points_ls[0]
        #     self.path = astar(self.env.grid, start=self.agent.position, goal=self.goal)
        #
        #     print(self.path)
        #     assert self.path
        #
        # elif self.path==[]:
        #     x, y = self.agent.position
        #     directions = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        #     random.shuffle(directions)
        #
        #     for (nx, ny) in directions:
        #         if 0 <= nx < self.env.width and 0 <= ny < self.env.height:
        #             cell = self.env.minigrid_env.grid.get(nx, ny)
        #             if cell is None:
        #                 self.agent.action = Actions.drop
        #
        # else:
        #     next_direction = self.path[0]
        #     turn_to_action = self.turn_to(next_direction)
        #     if turn_to_action == Actions.done:
        #         self.agent.action = Actions.forward
        #         self.path.pop(0)
        #     else:
        #         self.agent.action = turn_to_action
        #     print(self.path)


        x, y = self.agent.position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for (dx, dy) in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.env.width and 0 <= ny < self.env.height:
                cell = self.env.minigrid_env.grid.get(nx, ny)
                if cell is None:
                    turn_to_action = self.turn_to((dx, dy))
                    if turn_to_action == Actions.done:
                        self.agent.action = Actions.drop
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