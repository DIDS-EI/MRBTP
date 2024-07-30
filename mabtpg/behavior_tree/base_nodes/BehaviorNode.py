import py_trees as ptree
from typing import Any
import enum
from py_trees.common import Status


# base_nodes Behavior
class BahaviorNode(ptree.behaviour.Behaviour):
    is_composite = False
    can_be_expanded = True
    num_params = 0
    valid_params='''
        None
        '''
    print_name_prefix = ""


    def get_ins_name(self):
        args = self.args
        name = self.__class__.__name__
        if len(args) > 0:
            ins_name = f'{name}({",".join(map(str,args))})'
        else:
            ins_name = f'{name}()'
        return ins_name

    def __init__(self,*args):
        self.args = args
        ins_name = self.get_ins_name()

        self.agent = None
        self.env = None
        self.ins_name = ins_name
        super().__init__(ins_name)


    def bind_agent(self,agent):
        self.agent = agent
        self.env = agent.env

    def update(self) -> Status:
        print("this is just a base_nodes behavior node.")
        return Status.INVALID


    def setup(self, **kwargs: Any) -> None:
        return super().setup(**kwargs)

    def initialise(self) -> None:
        return super().initialise()

    def terminate(self, new_status: Status) -> None:
        return super().terminate(new_status)

    @property
    def draw_name(self):
        return self.name

    @property
    def print_name(self):
        return f'{self.print_name_prefix}{self.get_ins_name()}'

    @property
    def arg_str(self):
        return ",".join(self.args)