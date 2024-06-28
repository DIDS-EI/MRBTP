
from typing import Tuple
Point = Tuple[int, int]

class Object:
    def __init__(self, pos=None, **kwargs):
        self.id = 0
        self.pos = pos
        self.attribute_dict = {}
        self.attribute_dict.update(kwargs)

    # def can_overlap(self) -> bool:
    #     return False
    #
    # def can_pickup(self) -> bool:
    #     return False
    #
    # def can_contain(self) -> bool:
    #     return False
    #
    # def see_behind(self) -> bool:
    #     return True

    def toggle(self, env, pos: tuple[int, int]) -> bool:
        return False

    @property
    def instance_name(self):
        return self.__class__.__name__.lower() + "-id"

    def encode(self) -> str:
        return self.instance_name


