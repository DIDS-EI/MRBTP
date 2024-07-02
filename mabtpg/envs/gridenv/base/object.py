from typing import TYPE_CHECKING, Tuple

import numpy as np

from minigrid.core.constants import (
    COLOR_TO_IDX,
    COLORS,
    IDX_TO_COLOR,
    IDX_TO_OBJECT,
    OBJECT_TO_IDX,
)
from minigrid.utils.rendering import (
    fill_coords,
    point_in_circle,
    point_in_line,
    point_in_rect,
)

if TYPE_CHECKING:
    from minigrid.minigrid_env import MiniGridEnv

from typing import Tuple
Point = Tuple[int, int]

from mabtpg.envs.gridenv.base.icon import draw_icon
from mabtpg.envs.gridenv.base import Components


class Object:
    icon_folder_path = None

    def __init__(self, id=0, attribute_dict={}):
        self.id = id
        self.pos = (0,0)
        self.attribute_dict = {}
        self.attribute_dict.update(attribute_dict)
        self.set_components()
        self.get_components()

    def set_components(self):
        pass


    def can_overlap(self) -> bool:
        return False

    def can_pickup(self) -> bool:
        return False

    def can_contain(self) -> bool:
        return False

    def see_behind(self) -> bool:
        return True


    def toggle(self, env, pos: tuple[int, int]) -> bool:
        return False

    @property
    def instance_name(self):
        return self.__class__.__name__.lower() + f"-{self.id}"

    def encode(self) -> str:
        return self.instance_name

    def get_components(self):
        pass


    def get_component(self,component_name):
        if hasattr(self,component_name):
            return self.__getattribute__(component_name)
        return None


    def render(self, img):
        self.render_self(img)

        # render container
        container = self.get_component('container')
        if container:
            original_size = img.shape[0]
            num_contains = len(container.contain_list)
            scale = 0.6
            scaled_size = int(original_size * scale)

            if num_contains == 1:
                total_sub_size = scaled_size
                x_gap = 0
            else:
                total_sub_size = int(original_size * 0.9)
                x_gap = (total_sub_size - scaled_size) // (num_contains - 1)

            x_start = (original_size - total_sub_size) // 2

            positions = [(x_start + i * x_gap, (original_size - scaled_size) // 2) for i in range(num_contains)]

            for i in range(num_contains):
                position = positions[i]
                sub_img = img[position[1]:position[1] + scaled_size, position[0]:position[0] + scaled_size]
                container.contain_list[i].render(sub_img)

    def render_self(self,img):
        draw_icon(self.icon_folder_path, self.__class__.__name__, img)


COLORS = {
    "red": np.array([255, 0, 0]),
    "green": np.array([0, 255, 0]),
    "blue": np.array([0, 0, 255]),
    "purple": np.array([112, 39, 195]),
    "yellow": np.array([255, 255, 0]),
    "grey": np.array([100, 100, 100]),
}

class Wall(Object):
    def see_behind(self):
        return False

    def render(self, img):
        fill_coords(img, point_in_rect(0, 1, 0, 1), COLORS["grey"])


class Floor(Object):

    def set_components(self):
        self.container = Components.Container()

    def see_behind(self):
        return False

    def render_self(self, img):
        # Give the floor a pale color
        color = COLORS["grey"] / 2
        fill_coords(img, point_in_rect(0.031, 1, 0.031, 1), color)
