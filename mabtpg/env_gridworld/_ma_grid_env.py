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



# MiniGrid库最简单的可视化方法：命令行输入 python -m minigrid.manual_control --env BabyAI-BossLevelNoUnlock-v0，用键盘控制智能体






##################################
### 定义智能体 ###
##################################

# 定义智能体类
class Agent(object):
    def __init__(self,env=None):
        self.env = None
        self.action = None

        self.pos = (-1, -1)
        self.dir = -1
        self.carrying = None

    def bind_bt(self,bt):
        self.bt = bt
        bt.bind_agent(self)

    def step(self):
        self.bt.tick()
        return self.action

    # def step(self):
    #     if self.env.time > self.next_response_time:
    #         self.next_response_time += self.response_frequency
    #         self.step_num += 1
    #
    #         self.bt.tick()
    #         bt_output = self.bt.visitor.output_str
    #
    #         if bt_output != self.last_tick_output:
    #             if self.env.print_ticks:
    #                 print(f"==== time:{self.env.time:f}s ======")
    #
    #                 # print(bt_output)
    #                 # 分割字符串
    #                 parts = bt_output.split("Action", 1)
    #                 # 获取 'Action' 后面的内容
    #                 if len(parts) > 1:
    #                     bt_output = parts[1].strip()  # 使用 strip() 方法去除可能的前后空格
    #                 else:
    #                     bt_output = ""  # 如果 'Action' 不存在于字符串中，则返回空字符串
    #                 print("Action ",bt_output)
    #                 print("\n")
    #
    #                 self.last_tick_output = bt_output
    #             return True
    #         else:
    #             return False


##################################
### 定义环境 ###
##################################


class MAGrid(Grid):

    @classmethod
    def render_tile(
        cls,
        obj: WorldObj | None,
        agents_dir: tuple[int] | None = None,
        highlight: bool = False,
        tile_size: int = TILE_PIXELS,
        subdivs: int = 3,
    ) -> np.ndarray:
        """
        Render a tile and cache the result
        """

        # Hash map lookup key for the cache
        key: tuple[Any, ...] = (agents_dir, highlight, tile_size)
        key = obj.encode() + key if obj else key

        if key in cls.tile_cache:
            return cls.tile_cache[key]

        img = np.zeros(
            shape=(tile_size * subdivs, tile_size * subdivs, 3), dtype=np.uint8
        )

        # Draw the grid lines (top and left edges)
        fill_coords(img, point_in_rect(0, 0.031, 0, 1), (100, 100, 100))
        fill_coords(img, point_in_rect(0, 1, 0, 0.031), (100, 100, 100))

        if obj is not None:
            obj.render(img)

        # Overlay the agent on top
        if agents_dir is not None:
            for dir in agents_dir:
                tri_fn = point_in_triangle(
                    (0.12, 0.19),
                    (0.87, 0.50),
                    (0.12, 0.81),
                )

                # Rotate the agent based on its direction
                tri_fn = rotate_fn(tri_fn, cx=0.5, cy=0.5, theta=0.5 * math.pi * dir)
                fill_coords(img, tri_fn, (255, 0, 0))

        # Highlight the cell if needed
        if highlight:
            highlight_img(img)

        # Downsample the image to perform supersampling/anti-aliasing
        img = downsample(img, subdivs)

        # Cache the rendered tile
        cls.tile_cache[key] = img

        return img

    def render(
        self,
        agents,
        tile_size: int,
        highlight_mask: np.ndarray | None = None,
    ) -> np.ndarray:
        """
        Render this grid at a given scale
        :param r: target renderer object
        :param tile_size: tile size in pixels
        """

        if highlight_mask is None:
            highlight_mask = np.zeros(shape=(self.width, self.height), dtype=bool)

        agent_dir_dict = {}
        for agent in agents:
            if agent.pos not in agent_dir_dict:
                agent_dir_dict[agent.pos] = [agent.dir]
            else:
                agent_dir_dict[agent.pos] += [agent.dir]


        # Compute the total grid size
        width_px = self.width * tile_size
        height_px = self.height * tile_size

        img = np.zeros(shape=(height_px, width_px, 3), dtype=np.uint8)

        # Render the grid
        for j in range(0, self.height):
            for i in range(0, self.width):
                cell = self.get(i, j)
                # agents_dir = []
                # for agent in agents:
                #     if np.array_equal(agents[i].pos, (i, j)):
                #         agents_dir.append(agents[i].dir)
                if (i,j) in agent_dir_dict:
                    agents_dir = tuple(agent_dir_dict[(i,j)])
                else:
                    agents_dir = None

                assert highlight_mask is not None
                tile_img = MAGrid.render_tile(
                    cell,
                    agents_dir= agents_dir,
                    highlight=highlight_mask[i, j],
                    tile_size=tile_size,
                )

                ymin = j * tile_size
                ymax = (j + 1) * tile_size
                xmin = i * tile_size
                xmax = (i + 1) * tile_size
                img[ymin:ymax, xmin:xmax, :] = tile_img

        return img



class MAGridEnv(MiniGridEnv):
    def __init__(
        self,
        num_agent: int = 1,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.agent_pos = (-1, -1)
        self.agent_dir = -1
        self.num_agent = num_agent
        self.agents = [Agent(self) for _ in range(num_agent)]



    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[ObsType, dict[str, Any]]:
        gym.Env.reset(self,seed=seed)

        # Generate a new random grid at the start of each episode
        self._gen_grid(self.width, self.height)

        # These fields should be defined by _gen_grid
        # assert (
        #     self.agent_pos >= (0, 0)
        #     if isinstance(self.agent_pos, tuple)
        #     else all(self.agent_pos >= 0) and self.agent_dir >= 0
        # )

        # Check that the agent doesn't overlap with an object
        # start_cell = self.grid.get(*self.agent_pos)
        # assert start_cell is None or start_cell.can_overlap()

        # Item picked up, being carried, initially nothing
        self.carrying = None

        # Step count since episode start
        self.step_count = 0

        if self.render_mode == "human":
            self.render()

        # Return first observation
        obs = self.gen_obs()

        return obs, {}


    def env_step(self):
        pass

    def agent_step(self,action: ActType
    ) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        # reward = 0
        # terminated = False
        # truncated = False

        # Get the position in front of the agent
        fwd_pos = self.front_pos

        # Get the contents of the cell in front of the agent
        fwd_cell = self.grid.get(*fwd_pos)

        # Rotate left
        if action == self.actions.left:
            self.agent_dir -= 1
            if self.agent_dir < 0:
                self.agent_dir += 4

        # Rotate right
        elif action == self.actions.right:
            self.agent_dir = (self.agent_dir + 1) % 4

        # Move forward
        elif action == self.actions.forward:
            if fwd_cell is None or fwd_cell.can_overlap():
                self.agent_pos = tuple(fwd_pos)
            # if fwd_cell is not None and fwd_cell.type == "goal":
            #     terminated = True
            #     reward = self._reward()
            # if fwd_cell is not None and fwd_cell.type == "lava":
            #     terminated = True

        # Pick up an object
        elif action == self.actions.pickup:
            if fwd_cell and fwd_cell.can_pickup():
                if self.carrying is None:
                    self.carrying = fwd_cell
                    self.carrying.cur_pos = np.array([-1, -1])
                    self.grid.set(fwd_pos[0], fwd_pos[1], None)

        # Drop an object
        elif action == self.actions.drop:
            if not fwd_cell and self.carrying:
                self.grid.set(fwd_pos[0], fwd_pos[1], self.carrying)
                self.carrying.cur_pos = fwd_pos
                self.carrying = None

        # Toggle/activate an object
        elif action == self.actions.toggle:
            if fwd_cell:
                fwd_cell.toggle(self, fwd_pos)

        # Done action (not used by default)
        elif action == self.actions.done:
            pass

        else:
            raise ValueError(f"Unknown action: {action}")



    def step(self,action=None):
        self.step_count += 1
        truncated = False

        for i in range(self.num_agent):
            action = self.agents[i].step()
            # 执行单智能体与环境交互
            self.agent_pos = self.agents[i].pos
            self.agent_dir = self.agents[i].dir
            self.carrying = self.agents[i].carrying
            self.agent_step(action)
            self.agents[i].pos =self.agent_pos
            self.agents[i].dir = self.agent_dir
            self.agents[i].carrying = self.carrying

        if self.step_count >= self.max_steps:
            truncated = True

        if self.render_mode == "human":
            self.render()

        self.env_step()

        obs = self.gen_obs()
        return obs, None,None, {}


    def hash(self, size=16):
        """Compute a hash that uniquely identifies the current state of the environment.
        :param size: Size of the hashing
        """
        sample_hash = hashlib.sha256()

        to_encode = [self.grid.encode().tolist()]
        for agent in self.agents:
            carrying_type = agent.carrying.type if agent.carrying else None
            to_encode += [agent.pos, agent.dir,carrying_type]

        for item in to_encode:
            sample_hash.update(str(item).encode("utf8"))

        return sample_hash.hexdigest()[:size]




    def get_full_render(self, highlight, tile_size):
        """
        Render a non-paratial observation for visualization
        """
        # Mask of which cells to highlight
        highlight_mask = np.zeros(shape=(self.width, self.height), dtype=bool)

        for i in range(self.num_agent):
            self.agent_pos = self.agents[i].pos
            self.agent_dir = self.agents[i].dir

            # Compute which cells are visible to the agent
            _, vis_mask = self.gen_obs_grid()

            # Compute the world coordinates of the bottom-left corner
            # of the agent's view area
            f_vec = self.dir_vec
            r_vec = self.right_vec
            top_left = (
                self.agent_pos
                + f_vec * (self.agent_view_size - 1)
                - r_vec * (self.agent_view_size // 2)
            )

            # For each cell in the visibility mask
            for vis_j in range(0, self.agent_view_size):
                for vis_i in range(0, self.agent_view_size):
                    # If this cell is not visible, don't highlight it
                    if not vis_mask[vis_i, vis_j]:
                        continue

                    # Compute the world coordinates of this cell
                    abs_i, abs_j = top_left - (f_vec * vis_j) + (r_vec * vis_i)

                    if abs_i < 0 or abs_i >= self.width:
                        continue
                    if abs_j < 0 or abs_j >= self.height:
                        continue

                    # Mark this cell to be highlighted
                    highlight_mask[abs_i, abs_j] = True

        # Render the whole grid
        img = self.grid.render(
            self.agents,
            tile_size,
            highlight_mask=highlight_mask if highlight else None,
        )

        return img





    def place_agent(self, top=None, size=None, rand_dir=True, max_tries=math.inf):
        """
        Set the agent's starting point at an empty position in the grid
        """

        pos = self.place_obj(None, top, size, max_tries=max_tries)
        for i in range(self.num_agent):
            self.agents[i].pos = pos
            if rand_dir:
                self.agents[i].dir = self._rand_int(0, 4)

        return pos




##################################
### 用pygame可视化该环境 ###
##################################
if __name__ == '__main__':


    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--env-id",
        type=str,
        help="gym environment to load",
        choices=gym.envs.registry.keys(),
        default="MABTPG-Empty-16x16-v0",

    )
    parser.add_argument(
        "--seed",
        type=int,
        help="random seed to generate the environment with",
        default=None,
    )
    parser.add_argument(
        "--tile-size", type=int, help="size at which to render tiles", default=32
    )
    parser.add_argument(
        "--agent-view",
        action="store_true",
        help="draw the agent sees (partially observable view)",
    )
    parser.add_argument(
        "--agent-view-size",
        type=int,
        default=7,
        help="set the number of grid spaces visible in agent-view ",
    )
    parser.add_argument(
        "--screen-size",
        type=int,
        default="640",
        help="set the resolution for pygame rendering (width and height)",
    )

    args = parser.parse_args()

    env = gym.make(
        args.env_id,
        tile_size=args.tile_size,
        render_mode="human",
        agent_pov=args.agent_view,
        agent_view_size=args.agent_view_size,
        screen_size=args.screen_size,
    )

    # TODO: check if this can be removed
    if args.agent_view:
        print("Using agent view")
        env = RGBImgPartialObsWrapper(env, args.tile_size)
        env = ImgObsWrapper(env)

    env.reset(seed=0)
    env.render()




    # BT规划算法，这里就直接加载行为树
    from mabtpg.behavior_tree.behavior_tree import BehaviorTree
    from mabtpg.behavior_tree.behavior_library import BehaviorLibrary

    behavior_lib_path = f"../mabtpg/env_gridworld/behavior_lib"
    behavior_lib = BehaviorLibrary(behavior_lib_path)

    for agent in env.agents:
        bt = BehaviorTree("random.btml", behavior_lib)
        agent.bind_bt(bt)


    # 运行环境
    while True:
        env.step(None)
        # agent.bind_bt(bt)

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         env.close()
        #         break
        #     if event.type == pygame.KEYDOWN:
        #         event.key = pygame.key.name(int(event.key))
        #         # key_handler(event)

