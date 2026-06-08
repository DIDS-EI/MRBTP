from mabtpg.behavior_tree.base_nodes.BehaviorNode import BahaviorNode
from mabtpg.utils.tools import print_colored
from mabtpg.behavior_tree import Status
from mabtpg.behavior_tree.base_nodes import Action
class MinigridAction(Action):
    can_be_expanded = False

    def check_if_pre_in_predict_condition(self):

        act_pre = self.env.blackboard["action_pre"][self.name]

        # wait pre
        wait_cond = (act_pre & self.agent.predict_condition['success'])
        if  wait_cond!=set():
            if self.env.verbose: print_colored(f"{self.name}  Total Wait:{act_pre & self.agent.predict_condition['success']}",color="purple")
            return True
