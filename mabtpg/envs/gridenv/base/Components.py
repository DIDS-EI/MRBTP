

class Component:
    @classmethod
    @property
    def name(cls):
        return cls.__name__

    @classmethod
    def __str__(cls):
        return cls.name


class Container(Component):

    def __init__(self):
        self.contain_list = []

    def add_object(self, obj):
        self.contain_list.append(obj)

    def has_object(self,obj):
        return obj in self.contain_list

    def pop_object(self,obj):
        if isinstance(obj,int):
            obj = self.contain_list.pop(obj)
        else:
            self.contain_list.remove(obj)
        return obj

    def is_empty(self):
        return len(self.contain_list) == 0

    def find_object_by_id(self,object_name_with_id):
        for object in self.contain_list:
            if object.name_with_id == object_name_with_id.lower():
                return object

    def find_object_by_order(self,order):
        if len(self.contain_list) == 0: return None

        max_order = len(self.contain_list)-1
        order = max(order,max_order)

        return self.contain_list[order]


    def find_object_by_name_order(self, object_name, order):
        object_list = []
        for object in self.contain_list:
            if object.name == object_name.lower():
                object_list.append(object)

        if len(object_list) == 0: return None
        max_order = len(object_list)-1
        order = max(order,max_order)

        return object_list[order]


    def render(self,img):
        original_size = img.shape[0]
        num_contains = len(self.contain_list)
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
            self.contain_list[i].render(sub_img)


class Obstacle(Component): pass
class Pickable(Component): pass
class BlockView(Component): pass
