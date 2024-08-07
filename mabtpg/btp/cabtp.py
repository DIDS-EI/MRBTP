import copy

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
    def __init__(self,action_list,goal,sequence,id=None,verbose=False,env=None):
        super().__init__(action_list,goal,id,verbose)

        self.sequence = copy.deepcopy(sequence)
        self.sequence.reverse()

        self.sequence_index = 0

        self.collect_explored_cond_act = []

        self.env=env

    def one_step_expand(self, condition,seq_index):

        # Determine whether the expansion is within the tree or outside the tree before expanding!
        inside_condition = self.expanded_condition_dict.get(condition, None)

        # find premise conditions
        premise_condition_list = []
        cond_seqindex_ls = []

        for action in self.action_list:

            if seq_index+1 >= len(self.sequence):
                break

            # Ensures sequential expansion of actions in sub-action sequences
            if self.sequence[seq_index+1] not in action.name:
                continue

            if self.is_consequence(condition,action):

                premise_condition = frozenset((action.pre | condition) - action.add)
                if self.has_no_subset(premise_condition):

                    # conflict check
                    if self.env!=None:
                        if self.env.check_conflict(premise_condition):
                            continue


                    planning_condition = PlanningCondition(premise_condition,action.name)
                    premise_condition_list.append(planning_condition)
                    self.expanded_condition_dict[premise_condition] = planning_condition

                    # seq
                    planning_condition.parent_cond = condition
                    cond_seqindex_ls.append((premise_condition,seq_index+1))

                    # collcet
                    # self.collect_explored_cond_act.append((seq_index+1,planning_condition))
                    self.collect_explored_cond_act.append((seq_index + 1, planning_condition, action))

                    if self.verbose:
                        print_colored(f"---- Index:{seq_index+1}:  {action.name} ", "orange")

                    # if self.verbose:
                    #     if inside_condition:
                    #         print_colored(f'inside','purple')
                    #     else:
                    #         print_colored(f'outside','purple')
                    #     print_colored(f'a:{action.name} c_attr:{str(premise_condition)}','orange')

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
            cond_seqindex = explored_condition_list.pop(0)
            cond,seq_index = cond_seqindex
            if self.verbose: print_colored(f"C:{cond}  Index:{seq_index}", "green")
            premise_condition_list,cond_seqindex_ls = self.one_step_expand(cond,seq_index)
            explored_condition_list += cond_seqindex_ls
