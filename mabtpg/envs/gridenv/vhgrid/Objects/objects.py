
from mabtpg.envs.gridenv.vhgrid.base.vhgrid_object import VHGridObject

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    pass

Point = Tuple[int, int]

from mabtpg.envs.gridenv.base.object import *
from mabtpg.envs.gridenv.base.icon import draw_icon
from mabtpg.envs.gridenv.base.Components import Container
import numpy as np



def class_from_template(template_class, name):
    return type(name, (template_class,), {})


# class FruitTemplateClass(VHGridObject):
#     def __init__(self, name):
#         self.name = name
#
#     def greet(self):
#         print(f"Hello from {self.name}")

class PickableObject(VHGridObject):
    def set_components(self):
        self.add_component(Components.Pickable)



class Apple(PickableObject): pass
class Banana(PickableObject): pass
class Carrot(PickableObject): pass
class Cherry(PickableObject): pass





# fruit_class_names = ['apple', 'banana', 'cherry']
# classes = {}
#
# for name in fruit_class_names:
#     classes[name] = type(name, (TemplateClass,), {})
#
# # 实例化并使用这些类
# instances = [classes[name](name) for name in fruit_class_names]
#
# for instance in instances:
#     instance.greet()
