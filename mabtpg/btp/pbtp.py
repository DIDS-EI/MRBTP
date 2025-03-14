
from mabtpg.behavior_tree.behavior_tree import BehaviorTree
from mabtpg.utils import parse_predicate_logic
from mabtpg.utils.any_tree_node import AnyTreeNode
from mabtpg.behavior_tree.constants import NODE_TYPE
import re
import mabtpg
from mabtpg.utils.tools import print_colored
from mabtpg.behavior_tree import BTML

from mabtpg.btp.base import PlanningCondition, PlanningAgent

class PBTP(PlanningAgent):
    '''Behavior Tree Planning with Precondition'''
    def __init__(self,action_list,goal,id=None,verbose=False,precondition=None):
        super().__init__(action_list,goal,id,verbose)

        self.precondition = precondition

    def one_step_expand(self, condition):

        # Determine whether the expansion is within the tree or outside the tree before expanding!
        inside_condition = self.expanded_condition_dict.get(condition, None)

        # find premise conditions
        premise_condition_list = []
        for action in self.action_list:
            if self.is_consequence(condition,action):
                premise_condition = frozenset((action.pre | condition) - action.add)
                if self.has_no_subset(premise_condition):

                    # conflict check
                    if self.check_conflict(premise_condition):
                        continue

                    # If the plan conflicts with the precondition, it is considered a conflict
                    if self.precondition != None and self.check_conflict(premise_condition | self.precondition):
                        continue
                    # When planning, directly remove this condition.
                    if self.precondition != None:
                        if action.pre & self.precondition == set():
                            premise_condition -= self.precondition

                    planning_condition = PlanningCondition(premise_condition,action.name)
                    premise_condition_list.append(planning_condition)
                    self.expanded_condition_dict[premise_condition] = planning_condition

                    if self.verbose:
                        if inside_condition:
                            print_colored(f'inside','purple')
                        else:
                            print_colored(f'outside','purple')
                        print_colored(f'a:{action.name} \t c_attr:{premise_condition}','orange')

        # insert premise conditions into BT
        if inside_condition:
            self.inside_expand(inside_condition, premise_condition_list)
        else:
            self.outside_expand(premise_condition_list)

        return premise_condition_list


