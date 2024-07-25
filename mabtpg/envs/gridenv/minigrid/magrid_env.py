from __future__ import annotations

import gymnasium as gym

from minigrid.minigrid_env import MiniGridEnv
import numpy as np

import hashlib
import math
from typing import Any, SupportsFloat

from gymnasium.core import ActType, ObsType
from mabtpg.utils.tools import print_colored
from mabtpg.envs.gridenv.minigrid.agent import Agent
from minigrid.core.world_object import Point, WorldObj

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
        self.blackboard = {
            # other subgoal: the agent's subgoal
            # if some subgoal's dependency is the agent's subgoal, [other subgoal] cannot to regard success

            # task: task_id,subgoal
            "task_num":0, # 给所有任务编个号
            # "running_tasks":[],# [(1,x),(2,x)]

            # Each key is the task name, and the value is a list containing all tasks that depend on it as successors.
            # 每个键是任务名，值是一个包含所有受其依赖的后续任务的列表
            # (1,x) : [(2,x),(3,x),(4,x)]
            # (2,x) : [(3,x),(4,x),..]
            # ...
            # (8,x) : []
            "dependent_tasks_dic":{},

            # 记录每个任务的 dependency
            # (1,x): set
            # (2,x): set
            "task_predict_condition":{},
            "predict_condition": set(), # 总的假设空间


            "action_pre":{}
        }
        self.agents = [Agent(self,i) for i in range(num_agent)]


    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[ObsType, dict[str, Any]]:
        gym.Env.reset(self,seed=seed)

        # Generate a new random grid at the start of each episode
        self._gen_grid(self.width, self.height)

        # Item picked up, being carried, initially nothing
        self.carrying = None

        # Step count since episode start
        self.step_count = 0

        if self.render_mode == "human":
            self.render()

        # Return first observation
        obs = self.gen_obs()


        return obs, {}

    def set_focus_agent(self, agent:Agent):
        self.agent_pos = agent.position
        self.agent_dir = agent.direction
        self.carrying = agent.carrying

    def get_focus_agent(self, agent):
        agent.position = self.agent_pos
        agent.direction = self.agent_dir
        agent.carrying = self.carrying

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
            if fwd_cell is None or fwd_cell.type == "ball" or fwd_cell.type == "key" or fwd_cell.can_overlap():
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

    def step(self,action=None,num_agent = None):
        if num_agent is None:
            num_agent = self.num_agent
        self.step_count += 1
        done = True
        # truncated = False


        for i in range(num_agent):
            print_colored(f"---AGENT - {i}---",color="yellow")
            action = self.agents[i].step()
            # 执行单智能体与环境交互
            self.set_focus_agent(self.agents[i])
            self.agent_step(action)
            self.get_focus_agent(self.agents[i])
            print(f"agent {i}, {action.name}")

            if not self.agents[i].bt_success:
                done = False

        # if self.step_count >= self.max_steps:
        #     truncated = True

        if self.render_mode == "human":
            self.render()

        obs = self.gen_obs()
        return obs, done, None, {}


    def hash(self, size=16):
        """Compute a hash that uniquely identifies the current state of the environment.
        :param size: Size of the hashing
        """
        sample_hash = hashlib.sha256()

        to_encode = [self.grid.encode().tolist()]
        for agent in self.agents:
            carrying_type = agent.carrying.type if agent.carrying else None
            to_encode += [agent.position, agent.direction, carrying_type]

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
            self.agent_pos = self.agents[i].position
            self.agent_dir = self.agents[i].direction

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
            self.agents[i].position = pos
            if rand_dir:
                self.agents[i].direction = self._rand_int(0, 4)

        return pos

