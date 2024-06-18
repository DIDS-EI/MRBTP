from __future__ import annotations

import gymnasium as gym
import pygame
from gymnasium import Env

from minigrid.core.actions import Actions
from minigrid.minigrid_env import MiniGridEnv
from minigrid.wrappers import ImgObsWrapper, RGBImgPartialObsWrapper


from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Goal
from minigrid.minigrid_env import MiniGridEnv
from gymnasium.envs.registration import register

import math
from typing import Any, Callable

import numpy as np

from minigrid.core.constants import OBJECT_TO_IDX, TILE_PIXELS
from minigrid.core.world_object import Wall, WorldObj
from minigrid.utils.rendering import (
    downsample,
    fill_coords,
    highlight_img,
    point_in_rect,
    point_in_triangle,
    rotate_fn,
)

import hashlib
import math
from abc import abstractmethod
from typing import Any, Iterable, SupportsFloat, TypeVar


import pygame
import pygame.freetype
from gymnasium import spaces
from gymnasium.core import ActType, ObsType

from minigrid.core.actions import Actions
from minigrid.core.constants import COLOR_NAMES, DIR_TO_VEC, TILE_PIXELS
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Point, WorldObj

from mabtpg.env_gridworld._ma_grid_env import MAGridEnv,MAGrid

from minigrid.envs.babyai.core.roomgrid_level import BabyAIMissionSpace

T = TypeVar("T")

# MiniGrid库最简单的可视化方法：命令行输入 python -m minigrid.manual_control --env BabyAI-BossLevelNoUnlock-v0，用键盘控制智能体



class MiniGridToMAGridEnv(MAGridEnv):
    def __init__(
        self,
        minigrid_env: MiniGridEnv,
        num_agent: int = 1,
        **kwargs
    ):
        self.width = minigrid_env.width
        self.height = minigrid_env.height
        self.minigrid_env = minigrid_env

        super().__init__(mission_space=BabyAIMissionSpace(),
                         num_agent = num_agent,
                         grid_size = minigrid_env.width,
                         **kwargs)
        self.mission = minigrid_env.mission
        self.render_mode = "human"

    @staticmethod
    def _gen_mission():
        return "go"

    def _gen_grid(self, width, height):
        self.minigrid_env.reset()
        # self.minigrid_env._gen_grid(self.width, self.height)
        print(self.minigrid_env.agent_pos)
        print(self.minigrid_env.agent_dir)
        for i in range(self.num_agent):
            self.agents[i].pos = self.minigrid_env.agent_pos
            self.agents[i].dir = self.minigrid_env.agent_dir

        self.agent_pos = self.minigrid_env.agent_pos
        self.agent_dir = self.minigrid_env.agent_dir
        self.grid = self.minigrid_env.grid
        # self.grid.render = MAGrid(self.width, self.height).render.__get__(self.grid, Grid)

        self.grid.render = lambda *args,**kwargs: MAGrid.render(self.grid,*args,**kwargs)
        # self.grid = MAGridEnv()



