

class Component:
    pass



class Container(Component):

    def __init__(self):
        self.contain_list = []

    def add_obj(self,obj):
        self.contain_list.append(obj)

