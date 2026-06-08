# from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.envs.gridenv.minigrid.behavior_lib.base.Action import MinigridAction as Action
from mabtpg.behavior_tree import Status
from minigrid.core.actions import Actions
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.envs.gridenv.minigrid.utils import get_direction_index
import numpy as np
import random
from mabtpg.utils.astar import astar,is_near


class GoBtwRoom(Action):
    can_be_expanded = True
    num_args = 3
    valid_args = set()

    def __init__(self, agent_id,from_room_id,to_room_id):
        super().__init__(agent_id,from_room_id,to_room_id)
        self.path = None
        self.from_room_id = int(''.join(filter(str.isdigit, from_room_id)))  #from_room_id
        self.to_room_id = int(''.join(filter(str.isdigit, to_room_id))) #to_room_id
        self.goal = None



    @classmethod
    def get_planning_action_list(cls, agent, env):

        can_goto = env.cache["can_goto"]

        planning_action_list = []

        room_num = len(env.room_cells)
        # 通过单次遍历生成所有行动模型
        for door_id, (room1_id, room2_id) in env.doors_to_adj_rooms.items():
            # 处理从 room1 到 room2
            action_model = cls.create_action_model(agent.id, door_id, room1_id, room2_id, room_num, can_goto)
            planning_action_list.append(
                PlanningAction(f"GoBtwRoom(agent-{agent.id},room-{room1_id},room-{room2_id})", **action_model))

            # 处理从 room2 到 room1
            action_model = cls.create_action_model(agent.id, door_id, room2_id, room1_id, room_num, can_goto)
            planning_action_list.append(
                PlanningAction(f"GoBtwRoom(agent-{agent.id},room-{room2_id},room-{room1_id})", **action_model))
        return planning_action_list

    @classmethod
    def create_action_model(cls,agent_id, door_id, from_room_id, to_room_id, room_num, can_goto):
        action_model = {}
        action_model["pre"] = {f"IsInRoom(agent-{agent_id},room-{from_room_id})", f"IsOpen({door_id})"}
        action_model["add"] = {f"IsInRoom(agent-{agent_id},room-{to_room_id})"}
        action_model["del_set"] = {f'IsInRoom(agent-{agent_id},room-{rid})' for rid in range(room_num) if rid != to_room_id}
        action_model["del_set"] |= {f'IsNear(agent-{agent_id},{obj})' for obj in can_goto}
        action_model["cost"] = 1
        return action_model


    def update(self) -> Status:

        if self.check_if_pre_in_predict_condition():
            return Status.RUNNING

        if self.path is None:
            # Try every empty cell of the destination room (in random order) and
            # take the first one that is actually reachable.  Picking only one
            # cell up-front (the original behavior) crashed whenever it
            # happened to be blocked by other objects in the room.
            room_positions = list(self.env.room_cells[self.to_room_id])
            random.shuffle(room_positions)

            self.goal = None
            for pos in room_positions:
                x, y = pos
                if self.env.grid.get(x, y) is not None:
                    continue
                candidate = astar(self.env.grid, start=self.agent.position, goal=(x, y))
                if candidate is not None:
                    self.goal = (x, y)
                    self.path = candidate
                    break
            print(self.path)

            # Fallback: nothing in the room is reachable -> head for the door.
            if self.path is None:
                door_id = self.env.adj_rooms_to_doors[(self.from_room_id, self.to_room_id)]
                door_positions = list(self.env.id2obj[door_id].cur_pos)
                self.goal = tuple(door_positions)
                self.path = astar(self.env.grid, start=self.agent.position, goal=door_positions)
                print(self.path)

            # Last resort: even the door is unreachable this tick (e.g. another
            # agent is standing in the only walkable cell).  Stay put and
            # retry next tick instead of asserting.
            if self.path is None:
                if is_near(self.goal, self.agent.position):
                    goal_direction = np.array(self.goal) - np.array(self.agent.position)
                    self.agent.action = self.turn_to(goal_direction)
                else:
                    self.agent.action = Actions.done
                print("agent:", self.agent.id, " GoBtwRoom: no reachable cell, waiting")
                return Status.RUNNING

        if self.path == []:
            # goal_direction = self.goal - np.array(self.agent.position)
            # self.agent.action = self.turn_to(goal_direction)
            if is_near(self.goal, self.agent.position):
                goal_direction = self.goal - np.array(self.agent.position)
                self.agent.action = self.turn_to(goal_direction)
            else:
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
        print("agent:", self.agent.id, " GoBtwRoom:", self.from_room_id, self.to_room_id)
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

