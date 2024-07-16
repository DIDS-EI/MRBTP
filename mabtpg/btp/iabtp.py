
from mabtpg.behavior_tree.behavior_tree import BehaviorTree
from mabtpg.utils import parse_predicate_logic
from mabtpg.utils.any_tree_node import AnyTreeNode
from mabtpg.behavior_tree.constants import NODE_TYPE
import re
import mabtpg
from mabtpg.utils.tools import print_colored
from mabtpg.behavior_tree import BTML


class IABTP:
    def __init__(self,verbose=False):
        self.planned_agent_list = None
        self.verbose = verbose

    def planning(self, goal, action_lists,precondition=None):

        # If the plan conflicts with the precondition, it is considered a conflict
        self.precondition = precondition

        planning_agent_list = []
        for id,action_list in enumerate(action_lists):

            agent = PlanningAgent(action_list,goal,id,self.verbose,precondition = self.precondition)
            if self.verbose: print_colored(f"Agent:{agent.id}", "purple")
            planning_agent_list.append(agent)

            explored_condition_list = [goal]

            while explored_condition_list != []:
                condition = explored_condition_list.pop(0)
                if self.verbose: print_colored(f"C:{condition}","green")
                premise_condition_list = agent.one_step_expand(condition)
                explored_condition_list += [planning_condition.condition_set for planning_condition in premise_condition_list]

        self.planned_agent_list = planning_agent_list


    def output_bt_list(self,behavior_libs):
        bt_list = []
        for i,agent in enumerate(self.planned_agent_list):
            bt = agent.output_bt(behavior_libs[i])
            bt_list.append(bt)
        return bt_list