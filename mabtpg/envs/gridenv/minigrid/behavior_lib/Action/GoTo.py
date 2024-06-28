from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status
from minigrid.core.actions import Actions
from mabtpg.envs.gridenv.minigrid.objects import CAN_GOTO
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.envs.gridenv.minigrid.utils import obj_to_planning_name, get_direction_index
import numpy as np



class GoTo(Action):
    num_args = 2
    valid_args = [CAN_GOTO]

    def __init__(self, *args):
        super().__init__(*args)
        self.path = None
        self.goal = self.args[1].split("-")[-1].split("_")
        self.goal = list(map(int, self.goal))

    @classmethod
    def get_planning_action_list(cls, agent, env):
        planning_action_list = []
        if "can_goto" not in env.cache:
            env.cache["can_goto"] = []
            for obj in env.obj_list:
                if obj.type in cls.valid_args[0]:
                    env.cache["can_goto"].append(obj_to_planning_name(obj))

        can_goto = env.cache["can_goto"]
        for obj_planning_name in can_goto:
            action_model = {}
            action_model["pre"]= set()
            action_model["add"]={f"IsNear(agent_{agent.id},{obj_planning_name})"}
            action_model["del_set"] = {f'IsNear(agent_{agent.id},{obj_planning_name})' for obj in can_goto if obj != obj_planning_name}
            action_model["cost"] = 1
            planning_action_list.append(PlanningAction(f"GoTo(agent_{agent.id},{obj_planning_name})",**action_model))

        return planning_action_list


    def update(self) -> Status:
        if self.path is None:

            self.path = astar(self.env.grid, start=self.agent.pos, goal=self.goal)

            print(self.path)
            assert self.path

        if self.path == []:
            goal_direction = self.goal - np.array(self.agent.pos)
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
        diff = (direction_int - self.agent.dir) % 4

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


import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    rows, cols = grid.width, grid.height
    pq = []
    heapq.heappush(pq, (0 + heuristic(start, goal), 0, start, []))
    visited = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    goal_surroundings = [
        (goal[0] - 1, goal[1]),
        (goal[0] + 1, goal[1]),
        (goal[0], goal[1] - 1),
        (goal[0], goal[1] + 1)
    ]

    valid_goal_surroundings = [
        (x, y) for (x, y) in goal_surroundings if 0 <= x < rows and 0 <= y < cols and not grid.get(x, y)
    ]

    while pq:
        _, cost, (x, y), action_list = heapq.heappop(pq)

        if (x, y) in visited:
            continue

        visited.add((x, y))

        if (x, y) in valid_goal_surroundings:
            return action_list  # return action list

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols:
                cell = grid.get(nx, ny)

                if cell:
                    continue

                new_actions = action_list + [(dx, dy)]
                heapq.heappush(pq, (cost + 1 + heuristic((nx, ny), goal), cost + 1, (nx, ny), new_actions))

    return None