from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status
from minigrid.core.actions import Actions
from mabtpg.envs.gridenv.minigrid.objects import CAN_GOTO
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.envs.gridenv.minigrid.utils import get_direction_index
import numpy as np
from mabtpg.utils.astar import astar,is_near


class GoToInRoom(Action):
    can_be_expanded = True
    num_args = 2
    valid_args = [CAN_GOTO]

    def __init__(self, *args):
        super().__init__(*args)
        self.path = None

        self.agent_id = self.args[0]
        self.obj_id = self.args[1]
        self.room_id = self.args[2]


    @classmethod
    def get_planning_action_list(cls, agent, env):
        planning_action_list = []
        room_num = len(env.room_cells)
        can_goto = env.cache["can_goto"]

        for obj_id in can_goto:
            if "door" not in obj_id:
                room_index = env.get_room_index(env.id2obj[obj_id].cur_pos)
                planning_action_list.append(cls.create_action(agent.id, obj_id, room_index, can_goto, room_num))

        for door_id, (room1_id, room2_id) in env.doors_to_adj_rooms.items():
            for room_index in [room1_id, room2_id]:
                planning_action_list.append(cls.create_action(agent.id, door_id, room_index, can_goto, room_num))


        return planning_action_list

    @classmethod
    def create_action(cls, agent_id, target_id, room_index, can_goto, room_num):
        action_model = {
            "pre": {f"CanGoTo({target_id})", f"IsInRoom(agent-{agent_id},{room_index})"},
            "add": {f"IsNear(agent-{agent_id},{target_id})"},
            "del_set": {f'IsNear(agent-{agent_id},{obj})' for obj in can_goto if obj != target_id},
            "cost": 1
        }
        action_model["del_set"].update(
            {f'IsInRoom(agent-{agent_id},{rid})' for rid in range(room_num) if rid != room_index})
        return PlanningAction(f"GoToInRoom(agent-{agent_id},{target_id},{room_index})", **action_model)

    def update(self) -> Status:
        if self.path is None:
            # Find the specific location of an object on the map based on its ID
            self.goal = list(self.env.id2obj[self.obj_id].cur_pos)
            # print("obj_id:",self.obj_id,"\t goal:",self.goal,"\t agent.position",self.agent.position)

            self.path = astar(self.env.grid, start=self.agent.position, goal=self.goal)

            print(self.path)
            assert self.path

        if self.path == []:

            # check if is near
            if is_near(self.goal,self.agent.position):
                goal_direction = self.goal - np.array(self.agent.position)
                self.agent.action = self.turn_to(goal_direction)
            else:
                # print("obj_id:", self.obj_id, "\t goal:", self.goal, "\t agent.position", self.agent.position)
                # print("goal_direction:",self.goal - np.array(self.agent.position))
                self.path = None
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

