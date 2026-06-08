from mabtpg.behavior_tree.utils import Status
from mabtpg.behavior_tree.behavior_library import BehaviorLibrary

from mabtpg.envs.gridenv.base import Components

from mabtpg.envs.gridenv.base.object import Object
from mabtpg.envs.gridenv.base import Actions

from mabtpg.envs.gridenv.base.constants import DIR_TO_VEC
import math

from minigrid.utils.rendering import (
    downsample,
    fill_coords,
    highlight_img,
    point_in_rect,
    point_in_triangle,
    rotate_fn,
)


class Agent(Object):
    behavior_dict = {
        "Action": [],
        "Condition": []
    }

    def __init__(self,env=None,id=1,behavior_lib=None):
        super().__init__()
        self.env = env
        self.id = id
        if behavior_lib:
            self.behavior_lib = behavior_lib
        else:
            self.create_behavior_lib()

        self.bt = None
        self.bt_success = None

        self.position = (-1, -1)
        self.direction = 3
        self.carrying = None

        self.accept_task = None
        self.current_task = None

    def set_components(self):
        self.add_component(Components.Container)


    @property
    def direction_vector(self):
        assert (
                self.direction >= 0 and self.direction < 4
        ), f"Invalid agent_dir: {self.direction} is not within range(0, 4)"
        return DIR_TO_VEC[self.direction]

    @property
    def front_position(self):
        return self.position + self.direction_vector

    @property
    def front_object(self):
        return self.env.grid.get(*self.front_position)


    def create_behavior_lib(self):
        self.behavior_lib = BehaviorLibrary()
        self.behavior_lib.load_from_dict(self.behavior_dict)


    def bind_bt(self,bt):
        self.bt = bt
        bt.bind_agent(self)

    def step(self, action=None):
        if action is None:
            self.action = Actions.Idle
            if self.bt:
                self.current_task = None
                self.bt.tick()
                if self.current_task != self.accept_task:
                    self.env.blackboard["predict_condition"] -= self.accept_task
                self.bt_success = self.bt.root.status == Status.SUCCESS
        else:
            self.action = action
        return self.action


    def render_self(self,img):
        tri_fn = point_in_triangle(
            (0.12, 0.19),
            (0.87, 0.50),
            (0.12, 0.81),
        )

        # Rotate the agent based on its direction
        tri_fn = rotate_fn(tri_fn, cx=0.5, cy=0.5, theta=0.5 * math.pi * self.direction)
        fill_coords(img, tri_fn, (255, 0, 0))


    def encode(self):
        return f"{self.direction}_{super().encode()}"

class PickupAgent(Agent):
    pass