import py_trees as ptree
from mabtpg.behavior_tree.base_nodes.BehaviorNode import BahaviorNode, Status

class Condition(BahaviorNode):
    print_name_prefix = "condition "
    type = 'Condition'

    def __init__(self,*args):
        super().__init__(*args)

    def check_if_in_predict_condition(self)-> Status:

        # Other Agents Besides Myself
        # if self.agent.accept_task != None and self.name in self.agent.accept_task:
        #     return False
        # if self.name in self.env.blackboard["predict_condition"]:
        #     return True
        return False