
from mabtpg.behavior_tree.behavior_tree import BehaviorTree
from mabtpg.utils import parse_predicate_logic
from mabtpg.utils.any_tree_node import AnyTreeNode
from mabtpg.behavior_tree.constants import NODE_TYPE
import re
import mabtpg
from mabtpg.utils.tools import print_colored
from mabtpg.behavior_tree import BTML

from mabtpg.btp.base import PlanningCondition, PlanningAgent

class CABTP(PlanningAgent):
    '''Composition Action Behavior Tree Planning '''
    def __init__(self,action_list,goal,sub_act_ls,id=None,verbose=False):
        super().__init__(action_list,goal,id,verbose)

        reversed(sub_act_ls)
        self.sub_act_ls = sub_act_ls
        self.sub_act_index = len(sub_act_ls) - 1

        self.collect_explored_cond_act = []

    def one_step_expand(self, condition):

        # Determine whether the expansion is within the tree or outside the tree before expanding!
        inside_condition = self.expanded_condition_dict.get(condition, None)

        # find premise conditions
        premise_condition_list = []
        for action in self.action_list:

            if self.sub_act_index < 0:
                break

            if self.is_consequence(condition,action):
                premise_condition = frozenset((action.pre | condition) - action.add)
                if self.has_no_subset(premise_condition):

                    # conflict check
                    if self.check_conflict(premise_condition):
                        continue

                    # Ensures sequential expansion of actions in sub-action sequences
                    if self.sub_act_ls[self.sub_act_index] not in action.name:
                        continue
                    self.sub_act_index -= 1

                    planning_condition = PlanningCondition(premise_condition,action.name)
                    premise_condition_list.append(planning_condition)
                    self.expanded_condition_dict[premise_condition] = planning_condition

                    # collcet
                    self.collect_explored_cond_act.append((premise_condition,action))

                    if self.sub_act_index < 0:
                        break

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


