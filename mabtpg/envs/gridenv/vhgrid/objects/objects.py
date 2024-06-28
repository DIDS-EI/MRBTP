
from mabtpg.envs.gridenv.base.object import Object
from mabtpg.envs.gridenv.vhgrid.objects.icons import icon_folder_path

def class_from_template(template_class, name):
    return type(name, (template_class,), {})


class FruitTemplateClass(Object):
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Hello from {self.name}")

class Apple(Object):
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Hello from {self.name}")



class Objects:
    apple = Apple



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
