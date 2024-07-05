from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status
from minigrid.core.actions import Actions
from mabtpg.envs.gridenv.minigrid.objects import CAN_GOTO
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.envs.gridenv.minigrid.utils import obj_to_planning_name, get_direction_index
import numpy as np
import random
from mabtpg.envs.gridenv.minigrid.behavior_lib.Action.astar_algo import astar


class GoBtwRoom(Action):
    num_args = 2
    valid_args = set()

    def __init__(self, *args):
        super().__init__(*args)
        self.path = None
        self.from_room_id = int(self.args[1])
        self.to_room_id = int(self.args[2])
        self.goal = None


    @classmethod
    def get_planning_action_list(cls, agent, env):
        room_num = len(env.room_cells)

        planning_action_list = []

        for door_id,(from_room_id,to_room_id) in env.doors_to_adj_rooms.items():

            action_model = {}
            action_model["pre"]= {f"IsInRoom(agent-{agent.id},{from_room_id})",f"IsOpen({door_id})"}
            action_model["add"]={f"IsInRoom(agent-{agent.id},{to_room_id})"}
            action_model["del_set"] = {f'IsInRoom(agent-{agent.id},{rid})' for rid in range(room_num) if rid != to_room_id}


            action_model["cost"] = 1
            planning_action_list.append(PlanningAction(f"GoBtwRoom(agent-{agent.id},{from_room_id},{to_room_id})", **action_model))

        return planning_action_list


    def update(self) -> Status:
        if self.path is None:
            # Find the specific location of an object on the map based on its ID
            # self.arg_cur_pos = self.env.id2obj[self.obj_id].cur_pos
            # self.goal = list(self.arg_cur_pos)

            room_positions = self.env.room_cells[self.to_room_id]
            random.shuffle(room_positions)

            for pos in room_positions:
                x, y = pos
                cell = self.env.grid.get(x, y)
                if cell is None:
                    self.goal = (x, y)
                    break

            # consider cannot find a goal

            self.path = astar(self.env.grid, start=self.agent.position, goal=self.goal)

            print(self.path)
            assert self.path

        if self.path == []:
            goal_direction = self.goal - np.array(self.agent.position)
            self.agent.action = self.turn_to(goal_direction)
        else:
            next_direction = self.path[0]
            turn_to_action = self.turn_to(next_direction)
            if turn_to_action == Actions.done:
                self.agent.action = Actions.forward
                self.path.pop(0)
            else:
                self.agent.action = turn_to_action
            print(self.path)

        # self.agent.action = random.choice(list(Actions))
        # print(f"randomly do action: {self.agent.action.name}")
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

