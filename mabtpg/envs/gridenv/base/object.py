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
from mabtpg.envs.gridenv.base.Components import Component



class Object:
    icon_folder_path = None

    def __init__(self, id=0, attribute_dict={}):
        self.id = id
        self.position = (0, 0)
        self.attribute_dict = {}
        self.attribute_dict.update(attribute_dict)
        self.set_components()

    def set_components(self):
        pass

    def add_component(self,component_cls, *args,**kwargs):
        self.__setattr__(component_cls.name,component_cls(*args,**kwargs))

    @property
    def name(self):
        return self.__class__.__name__.lower()

    @property
    def name_with_id(self):
        return self.name + f"-{self.id}"

    def encode(self) -> str:
        encode_str = self.name_with_id
        if self.has_component(Components.Container):
            container = self.get_component(Components.Container)
            for object in container.contain_list:
                encode_str += f"_{object.encode()}"

        return encode_str

    def get_components(self):
        pass

    def has_component(self,component_cls):
        return hasattr(self,component_cls.name)


    def get_component(self,component_cls):
        if hasattr(self,component_cls.name):
            return self.__getattribute__(component_cls.name)
        return None


    def render(self, img):
        self.render_self(img)

        # render container
        container = self.get_component(Components.Container)
        if container:
            container.render(img)

    def render_self(self,img):
        draw_icon(self.icon_folder_path, self.__class__.__name__, img)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name_with_id == other
        if isinstance(other, Object):
            return self.name_with_id == other.name_with_id

        return False

class Wall(Object):

    def set_components(self):
        self.add_component(Components.BlockView)

    def render(self, img):
        fill_coords(img, point_in_rect(0, 1, 0, 1), COLORS["grey"])


class Floor(Object):

    def set_components(self):
        self.add_component(Components.Container)

    def see_behind(self):
        return False

    def render_self(self, img):
        # Give the floor a pale color
        color = COLORS["grey"] / 2
        fill_coords(img, point_in_rect(0.031, 1, 0.031, 1), color)
