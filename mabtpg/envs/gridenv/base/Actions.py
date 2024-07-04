from enum import Enum, auto
from mabtpg.envs.gridenv.base import Components
from mabtpg.envs.gridenv.base.object import Object
from mabtpg.envs.gridenv.base.constants import ID_DELIMITER, ORDER_DELIMITER


class Action:
    def __init__(self,*args):
        self.args = args

    def do(self, agent):
        pass

    def __str__(self):
        return self.name

    @property
    def name(self):
        arg_str = ",".join([str(arg) for arg in self.args])
        return f"{self.__class__.__name__.lower()}({arg_str})"



class Idle(Action):
    def __init__(self):
        super().__init__()


class Direction(Enum):
    left = -1
    right = 1

class Turn(Action):
    Direction = Direction

    def __init__(self,direction: Direction):
        super().__init__(direction)
        self.direction = direction

    def do(self, agent):
        agent.direction = (agent.direction + self.direction.value) % 4


class Forward(Action):
    def __init__(self):
        super().__init__()


    def do(self,agent):
        front_obj = agent.front_object

        if front_obj and front_obj.has_component(Components.Obstacle): return

        agent.position = agent.front_position


class PickUp(Action):
    def __init__(self,target_object=None):
        super().__init__()
        self.agent = None
        self.agent_container = None
        self.front_object = None
        self.front_container = None
        self.target_object = target_object

    def do(self,agent):
        self.agent = agent
        self.front_object = agent.front_object
        if self.front_object is None: return

        if self.front_object.has_component(Components.Container):
            self.front_container = self.front_object.get_component(Components.Container)

        self.agent_container = self.agent.get_component(Components.Container)

        if self.target_object is None:
            self.put_down_any_object()
        elif isinstance(self.target_object,Object):
            self.put_down_target_object()
        elif isinstance(self.target_object,str):
            self.put_down_str_object()
        elif isinstance(self.target_object,int):
            self.put_down_int_object()

    def put_down_any_object(self):
        if self.front_object.has_component(Components.Pickable):
            self.put_down_from_ground(self.front_object)
        elif self.front_container:
            self.put_down_from_container(self.front_object, 0)

    def put_down_target_object(self):
        if self.front_object == self.target_object:
        # object on ground
            self.put_down_from_ground(self.front_object)
        elif self.front_container:
        # object in a container
            if self.front_container.has_object(self.target_object):
                self.put_down_from_container(self.front_object,self.target_object)

    def put_down_str_object(self):
        target_str = self.target_object
        if ID_DELIMITER in target_str:
            if self.front_object.name_with_id == target_str:
                self.put_down_from_ground(self.front_object)
            elif self.front_container:
                target_object = self.front_container.find_object_by_id(target_str)
                if target_object:
                    self.put_down_from_container(self.front_object,target_object)
        elif ORDER_DELIMITER in target_str:
            target_name, order = target_str.split(ORDER_DELIMITER)
            self.put_down_object_by_name_order(target_name, order)
        else:
            self.put_down_object_by_name_order(target_str, 0)

    def put_down_int_object(self):
        if self.front_container is None:
            self.put_down_from_ground(self.front_object)
        else:
            target_object = self.front_container.find_object_by_order(self.target_object)
            if target_object:
                self.put_down_from_container(self.front_object,target_object)

    def put_down_object_by_name_order(self, target_name: str, order: int):
        if self.front_object.name == target_name:
            self.put_down_from_ground(self.front_object)
        elif self.front_container:
            target_object = self.front_container.find_object_by_name_order(target_name, order)
            if target_object:
                self.put_down_from_container(self.front_object, target_object)

    def put_down_from_ground(self,object):
        front_pos = self.agent.front_position
        self.agent.env.grid.set(*front_pos, None)

        agent_container = self.agent_container
        agent_container.add_object(object)

    def put_down_from_container(self,container_object,object):
        obj_container = container_object.get_component(Components.Container)
        put_down_object = obj_container.pop_object(object)

        agent_container = self.agent_container
        agent_container.add_object(put_down_object)


class PutDown(Action):
    def __init__(self,target_object=None):
        super().__init__()
        self.agent = None
        self.agent_container = None
        self.front_object = None
        self.front_container = None
        self.target_object = target_object


    def do(self,agent):
        self.agent = agent
        self.front_object = agent.front_object
        self.agent_container = self.agent.get_component(Components.Container)

        if self.agent_container.is_empty(): return

        if self.front_object:
            if not self.front_object.has_component(Components.Container):
                return
            else:
                self.front_container = self.front_object.get_component(Components.Container)

        self.get_target_object()
        if self.target_object is not None:
            self.put_down_target_object()



    def get_target_object(self):
        if self.target_object is None:
            self.target_object = self.agent_container.find_object_by_order(0)
        elif isinstance(self.target_object,Object):
            if not self.agent_container.has_object(self.target_object):
                self.target_object = None
        elif isinstance(self.target_object,str):
            if ID_DELIMITER in self.target_object:
                self.target_object = self.agent_container.find_object_by_id(self.target_object)
            elif ORDER_DELIMITER in self.target_object:
                target_name, order = self.target_object.split(ORDER_DELIMITER)
                self.target_object = self.agent_container.find_object_by_name_order(target_name, order)
            else:
                self.target_object = self.agent_container.find_object_by_name_order(self.target_object, 0)
        elif isinstance(self.target_object,int):
            self.target_object = self.agent_container.find_object_by_order(self.target_object)


    def put_down_target_object(self):
        if self.front_object is None:
        # put down object on ground
            self.put_down_to_ground(self.target_object)
        elif self.front_container:
        # put down object in to a container
            self.put_down_to_container(self.front_object, self.target_object)


    def put_down_to_ground(self, object):
        agent_container = self.agent_container
        put_down_object = agent_container.pop_object(object)

        front_pos = self.agent.front_position
        self.agent.env.grid.set(*front_pos, put_down_object)


    def put_down_to_container(self, container_object, object):
        agent_container = self.agent_container
        put_down_object = agent_container.pop_object(object)

        obj_container = container_object.get_component(Components.Container)
        obj_container.add_object(put_down_object)


