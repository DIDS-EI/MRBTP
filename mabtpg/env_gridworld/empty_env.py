from __future__ import annotations
from mabtpg.env_gridworld._ma_grid_env import MAGridEnv, MAGrid

from minigrid.core.world_object import Goal
from gymnasium.envs.registration import register

from minigrid.core.mission import MissionSpace


#定义一个空房间环境用来测试
class EmptyEnv(MAGridEnv):
    def __init__(
        self,
        size=8,
        num_agent=3,
        agents_start_pos=((1, 1), (2, 1), (6, 6)),
        agents_start_dir=(0, 1, 2),
        max_steps: int | None = None,
        **kwargs,
    ):
        self.agents_start_pos = agents_start_pos
        self.agents_start_dir = agents_start_dir

        mission_space = MissionSpace(mission_func=self._gen_mission)

        if max_steps is None:
            max_steps = 4 * size**2

        super().__init__(
            mission_space=mission_space,
            num_agent=num_agent,
            grid_size=size,
            # Set this to True for maximum speed
            see_through_walls=True,
            max_steps=max_steps,
            **kwargs,
        )



    @staticmethod
    def _gen_mission():
        return "get to the green goal square"

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = MAGrid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place a goal square in the bottom-right corner
        self.put_obj(Goal(), width - 2, height - 2)

        # Place the agent
        if self.agents_start_pos is not None:
            for i in range(self.num_agent):
                self.agents[i].pos = self.agents_start_pos[i]
                self.agents[i].dir = self.agents_start_dir[i]
        else:
            self.place_agent()

        self.mission = "get to the green goal square"


#注册该环境
register(
    id="MABTPG-Empty-16x16-v0",
    entry_point=__name__ + ":EmptyEnv",
    kwargs={"size": 16},
)



