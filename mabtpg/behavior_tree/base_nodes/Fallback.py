import py_trees as ptree
from typing import Any

class Fallback(ptree.composites.Selector):
    print_name = "fallback"
    ins_name = "Fallback"
    type = "Fallback"
    is_composite = True

    def __init__(self,*args,**kwargs):
        super().__init__(*args,name = "Fallback", **kwargs)

    def bind_agent(self,agent):
        pass