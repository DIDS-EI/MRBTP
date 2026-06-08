import py_trees as ptree
from mabtpg.behavior_tree.base_nodes.Condition import Condition, Status
from mabtpg.behavior_tree.base_nodes.Sequence import Sequence

class CompositeCondition(Condition):
    print_name_prefix = "condition "
    type = 'Condition'

    def __init__(self,cls_name,*args):
        self.cls_name = cls_name
        self.subtree = args[0]
        self.condition_list = self.subtree.root.children
        self.children_name_list = [c.ins_name for c in self.condition_list]
        self.children_name_list.sort()
        self.ins_name = " & ".join(self.children_name_list)
        super().__init__(*args)

    def get_ins_name(self):

        return self.ins_name

    def bind_agent(self,agent):
        self.agent = agent
        self.env = agent.env
        self.subtree.bind_agent(agent)


    def update(self) -> Status:
        self.subtree.tick()
        return self.subtree.root.status
