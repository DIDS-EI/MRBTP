from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status
from minigrid.core.actions import Actions
from mabtpg.envs.gridenv.minigrid.objects import CAN_GOTO
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.envs.gridenv.minigrid.utils import obj_to_planning_name, get_direction_index
import numpy as np
from mabtpg.envs.gridenv.minigrid.behavior_lib.Action.astar_algo import astar


class GoTo(Action):
    num_args = 2
    valid_args = [CAN_GOTO]

    def __init__(self, *args):
        super().__init__(*args)
        self.path = None
        self.obj_id = self.args[1]

        # self.arg_cur_pos = self.env.id2obj[self.args[1]].cur_pos
        # self.goal = list(self.arg_cur_pos)
        # self.goal = self.args[1].split("-")[-1].split("_")
        # self.goal = list(map(int, self.goal))

    @classmethod
    def get_planning_action_list(cls, agent, env):
        planning_action_list = []
        if "can_goto" not in env.cache:
            env.cache["can_goto"] = []
            for obj in env.obj_list:
                if obj.type in cls.valid_args[0]:
                    env.cache["can_goto"].append(obj.id)
                    # env.cache["can_goto"].append(obj_to_planning_name(obj))

        can_goto = env.cache["can_goto"]
        for obj_id in can_goto:
            action_model = {}
            action_model["pre"]= set()
            action_model["add"]={f"IsNear(agent-{agent.id},{obj_id})"}
            action_model["del_set"] = {f'IsNear(agent-{agent.id},{obj})' for obj in can_goto if obj != obj_id}

            # action_model["add"]={f"IsNear(agent-{agent.id},{obj_planning_name})"}
            # action_model["del_set"] = {f'IsNear(agent-{agent.id},{obj_planning_name})' for obj in can_goto if obj != obj_planning_name}

            action_model["cost"] = 1
            planning_action_list.append(PlanningAction(f"GoTo(agent-{agent.id},{obj_id})", **action_model))
            # planning_action_list.append(PlanningAction(f"GoTo(agent_{agent.id},{obj_planning_name})",**action_model))

        return planning_action_list


    def update(self) -> Status:
        if self.path is None:
            # Find the specific location of an object on the map based on its ID
            self.arg_cur_pos = self.env.id2obj[self.obj_id].cur_pos
            self.goal = list(self.arg_cur_pos)

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

