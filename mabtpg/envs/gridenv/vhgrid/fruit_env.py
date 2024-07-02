
from gymnasium.envs.registration import register
from mabtpg.envs.gridenv.vhgrid.base.vhgrid_env import VHGridEnv
from mabtpg.envs.gridenv.vhgrid import Agents
from mabtpg.envs.gridenv.vhgrid import Objects

class FruitEnv(VHGridEnv):
    agent_list = [Agents.GotoAgent]

    def __init__(self,**kwargs):
        self.agents_start_pos = ((1, 1), (2, 1), (6, 6))
        self.agents_start_dir = (0, 1, 2)

        super().__init__(**kwargs)

    def _gen_grid(self, width, height):
        #TODO: 智能体也是容器类
        #TODO: 物体的属性用集合来表示
        #TODO: 智能体的动作用类来表示
        super()._gen_grid(width,height)

        # objects
        self.add_obj(Objects.Apple(), 1, 5)
        self.add_obj(Objects.Banana(), 2, 5)
        self.add_obj(Objects.Carrot(), 3, 5)
        self.add_obj(Objects.Cherry(), 4, 5)

        floor = Objects.Floor()
        floor.container.add_obj(Objects.Banana())
        floor.container.add_obj(Objects.Cherry())
        floor.container.add_obj(Objects.Cherry())
        floor.container.add_obj(Objects.Apple())

        self.add_obj(floor, 6, 5)


        # 生成智能体
        if self.agents_start_pos is not None:
            for i in range(self.num_agent):
                self.agents[i].pos = self.agents_start_pos[i]
                self.agents[i].dir = self.agents_start_dir[i]
        else:
            self.place_agent()




register(
    id="MABTPG-Fruit-v0",
    entry_point=__name__ + ":FruitEnv",
)
