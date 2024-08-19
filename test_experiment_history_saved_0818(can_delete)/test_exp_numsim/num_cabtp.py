import copy

from mabtpg.btp.cabtp import CABTP
from mabtpg.behavior_tree.behavior_tree import BehaviorTree
from mabtpg.utils import parse_predicate_logic
from mabtpg.utils.any_tree_node import AnyTreeNode
from mabtpg.behavior_tree.constants import NODE_TYPE
import re
import mabtpg
from mabtpg.utils.tools import print_colored
from mabtpg.behavior_tree import BTML

from mabtpg.btp.base import PlanningCondition
from mabtpg.btp.base import PlanningAgent
from mabtp_test import PlanningAgentTest



# class Num_CABTP(PlanningAgentTest):
class Num_CABTP(PlanningAgent):
    '''Composition Action Behavior Tree Planning '''
    def __init__(self,goal,action_list,sequence,id=None,verbose=False):
        super().__init__(action_list, goal, id, verbose)
        self.sequence = copy.deepcopy(sequence)
        self.sequence.reverse()
        self.sequence_index = 0

        self.collect_explored_cond_act = []

        self.record_expanded_num = 0

    def one_step_expand(self, cond_seqindex):
        condition,seq_index = cond_seqindex
        # Determine whether the expansion is within the tree or outside the tree before expanding!
        inside_condition = self.expanded_condition_dict.get(condition, None)

        # find premise conditions
        premise_condition_list = []
        cond_seqindex_ls = []

        for action in self.action_list:

            if seq_index+1 >= len(self.sequence):
                break

            # Ensures sequential expansion of actions in sub-action sequences
            if self.sequence[seq_index+1].name != action.name:
                continue

            if self.is_consequence(condition,action):
            # if True:
                premise_condition = frozenset((action.pre | condition) - action.add)
                if self.has_no_subset(premise_condition):
                # if True:
                    # conflict check
                    if self.check_conflict(premise_condition):
                        continue


                    planning_condition = PlanningCondition(premise_condition,action.name)
                    premise_condition_list.append(planning_condition)
                    self.expanded_condition_dict[premise_condition] = planning_condition

                    # seq
                    planning_condition.parent_cond = condition
                    cond_seqindex_ls.append((premise_condition,seq_index+1))

                    # collcet
                    self.collect_explored_cond_act.append((seq_index + 1, planning_condition, action))

                    if self.verbose:
                        print_colored(f"---- Index:{seq_index+1}:  {action.name} ", "orange")


        # insert premise conditions into BT
        if inside_condition:
            self.inside_expand(inside_condition, premise_condition_list)
        else:
            self.outside_expand(premise_condition_list)

        return premise_condition_list,cond_seqindex_ls

    def planning(self):
        # cond,index
        explored_condition_list = [(self.goal,-1)]

        while explored_condition_list != []:
            self.record_expanded_num +=1
            cond_seqindex = explored_condition_list.pop(0)
            cond,seq_index = cond_seqindex
            if self.verbose: print_colored(f"C:{cond}  Index:{seq_index}", "green")
            premise_condition_list,cond_seqindex_ls = self.one_step_expand(cond_seqindex)
            explored_condition_list += cond_seqindex_ls
