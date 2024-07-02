

from mabtpg.envs.gridenv.minigrid.magrid_env import MAGridEnv
from mabtpg.envs.gridenv.minigrid.magrid import MAGrid


from minigrid.core.mission import MissionSpace
from minigrid.envs.babyai.core.verifier import *

from mabtpg import BehaviorLibrary

from mabtpg.envs.gridenv.minigrid.utils import obj_to_planning_name


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
        self.instrs = minigrid_env.instrs

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

    def initialize_objects(self):
        # Initialize dictionaries for counting object types and mapping names to IDs
        self.obj_type_num = {}
        self.id2obj = {}
        self.obj_name2id = {}
        self.obj_id2name={}

        # Assign IDs and count object types
        for obj in self.obj_list:
            # Add a private 'id' attribute to each object in the list if it doesn't already have one
            if not hasattr(obj, 'id') or obj.id is None:
                if obj.type not in self.obj_type_num:
                    self.obj_type_num[obj.type] = 0
                obj.id = f"{obj.type}{self.obj_type_num[obj.type]}"
                self.obj_type_num[obj.type] += 1

                self.id2obj[obj.id] = obj

            obj.name = obj_to_planning_name(obj)
            self.obj_name2id[obj.name] = obj.id

        self.obj_id2name = {id_: name for name, id_ in self.obj_name2id.items()}


    def _gen_grid(self, width, height):
        # self.minigrid_env._gen_grid(self.width, self.height)

        for i in range(self.num_agent):
            self.agents[i].pos = self.minigrid_env.agent_pos
            self.agents[i].dir = self.minigrid_env.agent_dir

        self.agent_pos = self.minigrid_env.agent_pos
        self.agent_dir = self.minigrid_env.agent_dir
        self.grid = self.minigrid_env.grid
        # self.grid.render = MAGrid(self.width, self.height).render.__get__(self.grid, Grid)

        self.grid.render = lambda *args,**kwargs: MAGrid.render(self.grid,*args,**kwargs)
        # self.grid = MAGridEnv()


    def get_goal(self):
        name = f"{self.instrs.desc.color}_{self.instrs.desc.type}"
        x, y = self.instrs.desc.obj_set[0].cur_pos
        planning_name = f"{name}-{x}_{y}"

        # Check if the planning name exists in the name-to-ID mapping
        if planning_name in self.obj_name2id:
            obj_id = self.obj_name2id[planning_name]
        else:
            # If not found, assign a default ID using the type from instruction's descriptor with suffix '0'
            obj_id = str(self.instrs.desc.type) + "0"

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

    def get_action_lists(self):
        obj_list = []
        self.cache = {}
        # list all Objects in env
        for i in range(self.grid.width):
            for j in range(self.grid.height):
                cell = self.grid.get(i, j)
                if cell is None:
                    continue

                if cell.type != "wall":
                    obj_list.append(cell)

        print("\n" + "-" * 10 + " Objects in the env " + "-" * 10)
        for obj in obj_list:
            print(obj.type,obj.cur_pos[0],obj.cur_pos[1])

        self.obj_list = obj_list

        # Initialize dictionaries for counting object types and mapping names to IDs
        self.initialize_objects()


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

        return action_list
