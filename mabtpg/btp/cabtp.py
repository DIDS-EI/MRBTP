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
    def __init__(self,action_list,goal,id=None,verbose=False,env=None):
        super().__init__(action_list,goal,id,verbose)

        self.action_list = copy.deepcopy(action_list)
        self.action_list.reverse()

        self.collect_explored_cond_act = []
        self.env=env

    def one_step_expand(self, planning_condition, next_action):

        premise_condition_list = []
        condition = planning_condition.condition_set
        if self.is_consequence(condition,next_action):
            premise_condition = frozenset((next_action.pre | condition) - next_action.add)
            if self.has_no_subset(premise_condition):

                # conflict check
                if self.env!=None:
                    if self.env.check_conflict(premise_condition):
                        return None


                new_planning_condition = PlanningCondition(premise_condition,next_action.name)
                premise_condition_list.append(new_planning_condition)
                self.expanded_condition_dict[premise_condition] = new_planning_condition
                # seq
                new_planning_condition.parent_cond = planning_condition

                self.inside_expand(planning_condition, premise_condition_list)

                return new_planning_condition

        return None


    def planning(self):


        self.goal_condition = PlanningCondition(self.goal)
        cond = self.goal_condition
        for planning_action in self.action_list:
            if self.verbose: print_colored(f"C:{cond}  Index:{planning_action.name}", "green")
            cond = self.one_step_expand(cond,planning_action)
            if cond is None:
                return None

        return True
