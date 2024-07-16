import random
import io
from mabtpg.envs.gridenv.minigrid.magrid_env import MAGridEnv
from mabtpg.envs.gridenv.minigrid.magrid import MAGrid


from minigrid.core.mission import MissionSpace
from minigrid.envs.babyai.core.verifier import *

from mabtpg import BehaviorLibrary

from mabtpg.envs.gridenv.minigrid.utils import obj_to_planning_name
from typing import Any, SupportsFloat
from gymnasium.core import ActType, ObsType
from mabtpg.envs.gridenv.minigrid.objects import CAN_GOTO,CAN_PICKUP,CAN_TOGGLE

# Quick start. Run this in console: python -m minigrid.manual_control --env BabyAI-BossLevelNoUnlock-v0

def gen_mission_func(env):
    def _gen_mission():
        return env.mission
    return _gen_mission


class MiniGridToMAGridEnv(MAGridEnv):
    def __init__(
        self,
        minigrid_env: MiniGridEnv,
        num_agent: int = 1,
        **kwargs
    ):
        self.width = minigrid_env.width
        self.height = minigrid_env.height

        minigrid_env.reset()
        self.minigrid_env = minigrid_env

        self.actions_lists = None


        # self.instrs = minigrid_env.instrs
        self.instrs = getattr(minigrid_env, 'instrs', None)


        mission_space = MissionSpace(mission_func=gen_mission_func(minigrid_env))

        super().__init__(mission_space=mission_space,
                         num_agent = num_agent,
                         grid_size = minigrid_env.width,

                         tile_size=minigrid_env.tile_size,
                         render_mode=None,
                         agent_view_size=minigrid_env.agent_view_size,
                         screen_size=minigrid_env.screen_size,

                         **kwargs)
        self.render_mode = "human"
        self.create_behavior_libs()

        # Assign cells to rooms
        self.room_cells,self.cells_room = self.assign_cells_to_rooms()


        ## need to put in after reset()
        # self.get_objects_lists()
        # self.adj_rooms_doors = self.get_adjacent_rooms_and_doors()

    def reset(
            self,
            *,
            seed: int | None = None,
            options: dict[str, Any] | None = None,
    ) -> tuple[ObsType, dict[str, Any]]:
        super().reset(seed=seed, options=options)

        self.get_objects_lists()
        # self.adj_rooms_doors = self.get_adjacent_rooms_and_doors()


    def assign_cells_to_rooms(self):
        """
        Assign walkable positions to different rooms in the MiniGridEnv environment.

        Returns:
            dict: A dictionary where keys are room indices and values are lists of walkable cell positions.
        """
        width, height = self.minigrid_env.grid.width, self.minigrid_env.grid.height
        visited = set()
        room_cells = {}

        def dfs(x, y, room_index):
            stack = [(x, y)]
            while stack:
                cx, cy = stack.pop()
                if (cx, cy) in visited:
                    continue
                visited.add((cx, cy))
                if room_index not in room_cells:
                    room_cells[room_index] = []
                room_cells[room_index].append((cx, cy))
                for nx, ny in [(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)]:
                    if 0 <= nx < width and 0 <= ny < height:
                        if (nx, ny) in visited: continue
                        cell = self.minigrid_env.grid.get(nx, ny)
                        if cell is None:
                            stack.append((nx, ny))
                        elif cell.type != "wall" and cell.type != "door":
                            stack.append((nx, ny))

        room_index = 0
        for i in range(width):
            for j in range(height):
                cell = self.minigrid_env.grid.get(i, j)
                if (i,j) in visited: continue
                if cell is None:
                    dfs(i, j, room_index)
                    room_index += 1
                elif cell.type != "wall" and cell.type != "door":
                    dfs(i, j, room_index)
                    room_index += 1

        cells_room = {}
        for room_index, cells in room_cells.items():
            for cell in cells:
                cells_room[cell] = room_index

        return room_cells,cells_room


    def get_room_index(self, pos):
        """
        Given a position (i, j), return the room index.

        Args:
            i (int): The x-coordinate of the position.
            j (int): The y-coordinate of the position.

        Returns:
            int: The index of the room that the position belongs to, or -1 if the position is not walkable.
        """
        # i,j = pos
        # for room_index, cells in self.room_cells.items():
        #     if (i, j) in cells:
        #         return room_index
        if isinstance(pos, np.ndarray):
            pos = tuple(pos.tolist())
        if pos in self.cells_room:
            return self.cells_room[pos]
        return -1

    def place_object_in_room(self, obj, room_index):
        """
        Place an object in a random position in the specified room.

        Args:
            room_index (int): The index of the room.
            obj (WorldObj): The object to place.

        Returns:
            tuple: The position where the object was placed, or None if no valid position was found.
        """
        if room_index not in self.room_cells:
            raise ValueError(f"Room index {room_index} does not exist.")

        room_positions = self.room_cells[room_index]
        random.shuffle(room_positions)

        for pos in room_positions:
            x, y = pos
            cell = self.minigrid_env.grid.get(x, y)
            if cell is None:
                self.minigrid_env.grid.set(x, y, obj)
                obj.cur_pos = (x, y)
                return (x, y)

        return None

    def initialize_objects_name_id(self):
        # Initialize dictionaries for counting object types and mapping names to IDs
        self.obj_type_num = {}
        self.id2obj = {}
        self.obj_name2id = {}
        self.obj_id2name={}

        # Initialize a dictionary to map doors to their corresponding keys
        self.door_key_map = {}
        self.key_door_map = {}
        # Temporary storage for locked doors and keys
        locked_doors = {}
        keys = {}

        # Assign IDs and count object types
        for obj in self.obj_list:
            # Add a private 'id' attribute to each object in the list if it doesn't already have one
            if not hasattr(obj, 'id') or obj.id is None:
                if obj.type not in self.obj_type_num:
                    self.obj_type_num[obj.type] = 0
                obj.id = f"{obj.type}-{self.obj_type_num[obj.type]}"
                self.obj_type_num[obj.type] += 1

            self.id2obj[obj.id] = obj
            obj.name = obj_to_planning_name(obj)
            self.obj_name2id[obj.name] = obj.id

            # Record locked doors and keys
            if obj.type == 'door' and obj.is_locked:
                locked_doors[obj.id] = obj.color
            elif obj.type == 'key':
                keys[obj.color] = obj.id

        # Bind locked doors to their corresponding keys
        for door_id, door_color in locked_doors.items():
            if door_color in keys:
                self.door_key_map[door_id] = keys[door_color]
        self.key_door_map = {key_id: door_id for door_id, key_id in self.door_key_map.items()}


        self.obj_id2name = {id_: name for name, id_ in self.obj_name2id.items()}


    def get_adjacent_rooms_and_doors(self):
        """
        Get all adjacent rooms and their connecting doors.

        Returns:
            list: A list of tuples (from_room_id, to_room_id, door_id).
        """
        doors_to_adj_rooms = {}
        adj_rooms_to_doors = {}
        door_positions = []

        for obj in self.obj_list:
            if obj.type == 'door':
                door_positions.append((obj.cur_pos[0], obj.cur_pos[1], obj.id))

        width, height = self.minigrid_env.grid.width, self.minigrid_env.grid.height
        for (i, j, door_id) in door_positions:
            adjacent_rooms = set()
            for nx, ny in [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]:
                if 0 <= nx < width and 0 <= ny < height:
                    for room_id, positions in self.room_cells.items():
                        if (nx, ny) in positions:
                            adjacent_rooms.add(room_id)
            if len(adjacent_rooms) == 2:
                from_room_id, to_room_id = tuple(adjacent_rooms)
                doors_to_adj_rooms[door_id] = (from_room_id, to_room_id)
                adj_rooms_to_doors[(from_room_id, to_room_id)] = door_id

        return doors_to_adj_rooms,adj_rooms_to_doors


    def _gen_grid(self, width, height):
        # self.minigrid_env._gen_grid(self.width, self.height)

        for i in range(self.num_agent):
            self.agents[i].position = self.minigrid_env.agent_pos
            self.agents[i].direction = self.minigrid_env.agent_dir

        self.agent_pos = self.minigrid_env.agent_pos
        self.agent_dir = self.minigrid_env.agent_dir
        self.grid = self.minigrid_env.grid
        # self.grid.render = MAGrid(self.width, self.height).render.__get__(self.grid, Grid)

        self.grid.render = lambda *args,**kwargs: MAGrid.render(self.grid,*args,**kwargs)
        # self.grid = MAGridEnv()


    def get_goal(self):

        if self.instrs==None:
            return None

        name = f"{self.instrs.desc.color}_{self.instrs.desc.type}"
        x, y = self.instrs.desc.obj_set[0].cur_pos
        planning_name = f"{name}-{x}_{y}"

        # Check if the planning name exists in the name-to-ID mapping
        if planning_name in self.obj_name2id:
            obj_id = self.obj_name2id[planning_name]
        else:
            # If not found, assign a default ID using the type from instruction's descriptor with suffix '0'
            obj_id = str(self.instrs.desc.type) + "-0"

        if isinstance(self.instrs, GoToInstr):
            return {f"IsNear(agent-0,{obj_id})", }
        if isinstance(self.instrs, PickupInstr):
            return {f"IsHolding(agent-0,{obj_id})"}

    def create_behavior_libs(self):
        from mabtpg.utils import get_root_path
        root_path = get_root_path()


        behavior_lib_path = f"{root_path}/envs/gridenv/minigrid/behavior_lib"
        behavior_lib = BehaviorLibrary(behavior_lib_path)
        for agent in self.agents:
            agent.behavior_lib = behavior_lib

    def get_objects_lists(self):
        obj_list = []
        self.cache = {}
        # list all Objects in env
        for i in range(self.grid.width):
            for j in range(self.grid.height):
                cell = self.grid.get(i, j)
                if cell is None:
                    continue

                if cell.type != "wall":
                    if cell.cur_pos == None:
                        cell.cur_pos = (i,j)
                    obj_list.append(cell)

        print("\n" + "-" * 10 + " Objects in the env " + "-" * 10)
        for obj in obj_list:
            # if obj.cur_pos==None:
            #     print(obj.type)
            # else:
            print(obj.type,obj.cur_pos[0],obj.cur_pos[1])

        self.obj_list = obj_list

        # Initialize dictionaries for counting object types and mapping names to IDs
        self.initialize_objects_name_id()

    def initialize_object_list(self, key, valid_types):
        """
        Initialize and cache a list of objects of specified types in the environment.
        """
        if key not in self.cache:
            self.cache[key] = [obj.id for obj in self.obj_list if obj.type in valid_types]
        return self.cache[key]

    def initialize_cache(self):
        """
        Utilize the generic helper function to initialize all relevant object lists.
        """
        can_goto = self.initialize_object_list("can_goto", CAN_GOTO)
        can_pickup = self.initialize_object_list("can_pickup", CAN_PICKUP)
        can_toggle = self.initialize_object_list("can_toggle", CAN_TOGGLE)
        return can_goto, can_pickup, can_toggle


    def get_action_lists(self):

        self.get_objects_lists()
        self.doors_to_adj_rooms,self.adj_rooms_to_doors = self.get_adjacent_rooms_and_doors()

        # obj cache
        can_goto, can_pickup, can_toggle = self.initialize_cache()

        # generate action list for all Agents
        action_list = []
        for i in range(self.num_agent):
            print("\n" + "-"*10 + f" getting action list for agent_{i} " + "-"*10)
            action_list.append([])
            for cls in self.agents[i].behavior_lib["Action"].values():
                if cls.can_be_expanded:
                    agent_action_list = cls.get_planning_action_list(self.agents[i], self)
                    action_list[i] += agent_action_list
                    print(f"action: {cls.__name__}, got {len(agent_action_list)} instances.")

            print(f"full action list ({len(action_list[i])} in total):")
            for a in action_list[i]:
                print(a.name)
                # print(a.name,"pre:",a.pre)

        return action_list

    def get_map(self):
        width, height = self.minigrid_env.grid.width, self.minigrid_env.grid.height
        cell_width = 10   # Set the width of each cell
        map_string = io.StringIO()  # Use StringIO to construct the string

        # Determine the positions of agents
        pos2angent_dic={}
        for agent in self.agents:
            pos = agent.position
            if not isinstance(pos, tuple):  # Check if pos is not a tuple
                raise TypeError("The variable 'pos' must be of type tuple")
            if pos in pos2angent_dic:
                pos2angent_dic[pos].append(str(agent.id))
            else:
                pos2angent_dic[pos] = [(str(agent.id))]


        for j in range(height):
            for i in range(width):
                cell = self.minigrid_env.grid.get(i, j)
                pos = (i,j)
                if pos in pos2angent_dic:
                    pos = (i, j)
                    agents_str = "agent-"+','.join(pos2angent_dic[pos])
                    map_string.write(f"{agents_str:<{cell_width}}")
                    continue
                if cell is None:
                    map_string.write(f"{' . ':<{cell_width}}")
                elif cell.type == "wall":
                    map_string.write(f"{' WALL ':<{cell_width}}")
                    # map_string.write(f"{' # ':<{cell_width}}")
                else:
                    map_string.write(f"{cell.id:<{cell_width}}")
            map_string.write("\n")  # Add newline character

        map_str = map_string.getvalue()  # Get the complete string
        map_string.close()  # Close the StringIO object
        return map_str