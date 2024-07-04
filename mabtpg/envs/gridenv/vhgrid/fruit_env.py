
from gymnasium.envs.registration import register
from mabtpg.envs.gridenv.vhgrid.base.vhgrid_env import VHGridEnv
from mabtpg.envs.gridenv.vhgrid import Agents, Objects, Components



class FruitEnv(VHGridEnv):
    agent_list = [Agents.GotoAgent]

    def __init__(self,**kwargs):
        self.agents_start_pos = ((1, 1), (2, 1), (6, 6))
        self.agents_start_dir = (1, 1, 2)

        super().__init__(**kwargs)

    def _gen_grid(self, width, height):
        #TODO: 智能体也是容器类， 画出物体跟随智能体
        #TODO: 智能体的动作用类来表示
        super()._gen_grid(width,height)

        # objects
        self.add_object(Objects.Apple(), 1, 5)
        self.add_object(Objects.Banana(), 2, 5)
        self.add_object(Objects.Carrot(), 3, 5)
        self.add_object(Objects.Cherry(), 4, 5)

        floor = Objects.Floor()
        floor_container = floor.get_component(Components.Container)

        floor_container.add_object(Objects.Banana())
        floor_container.add_object(Objects.Cherry())
        floor_container.add_object(Objects.Cherry())
        floor_container.add_object(Objects.Apple())

        self.add_object(floor, 6, 5)

        if self.agents_start_pos is not None:
            for i in range(self.num_agent):
                self.agents[i].position = self.agents_start_pos[i]
                self.agents[i].direction = self.agents_start_dir[i]
        else:
            self.place_agent()

        agent_container = self.agents[0].get_component(Components.Container)
        agent_container.add_object(Objects.Apple())



register(
    id="MABTPG-Fruit-v0",
    entry_point=__name__ + ":FruitEnv",
)
