
from mabtpg.behavior_tree.behavior_tree import BehaviorTree
from mabtpg.utils import parse_predicate_logic
from mabtpg.utils.any_tree_node import AnyTreeNode
from mabtpg.behavior_tree.constants import NODE_TYPE
import re
import mabtpg
from mabtpg.utils.tools import print_colored
from mabtpg.behavior_tree import BTML
from mabtpg.btp.base.planning_agent import PlanningAgent

from mabtpg.btp.mabtp import MABTP
from mabtpg.btp.base.planning_condition import PlanningCondition
import heapq

#


class CondCostPair:
    def __init__(self, cond,cost):
        self.cond = cond
        self.cost = cost
    def __lt__(self, other):
        # Define priority comparison: compare based on the value of cost.
        return self.cost < other.cost

class BfsPlanningAgent(PlanningAgent):
    def __init__(self,action_list,goal,id=None,verbose=False,start = None):
        self.id = id
        self.action_list = action_list
        self.expanded_condition_dict = {}
        self.goal = goal
        self.goal_condition = PlanningCondition(goal)
        self.expanded_condition_dict[goal] = self.goal_condition

        self.verbose = verbose

        self.start = start # ???delete

    def one_step_expand(self, condition_cost):

        # Determine whether the expansion is within the tree or outside the tree before expanding!
        condition, cost = condition_cost.cond, condition_cost.cost
        inside_condition = self.expanded_condition_dict.get(condition, None)

        # find premise conditions
        premise_condition_list = []
        premise_condition_cost_list=[]
        for action in self.action_list:
            if self.is_consequence(condition,action):
                premise_condition = frozenset((action.pre | condition) - action.add)
                if self.has_no_subset(premise_condition):

                    # conflict check
                    if self.check_conflict(premise_condition):
                        continue

                    # record if it is composition action
                    composition_action_flag = False
                    sub_goal = None
                    if action.cost==0:
                        composition_action_flag = True
                        # sub_goal = frozenset((action.pre | action.add) - action.del_set)
                        # sub_goal = [",".join(sorted(premise_condition))]
                        sub_goal = [premise_condition]

                    planning_condition = PlanningCondition(premise_condition,action.name,composition_action_flag,sub_goal)
                    premise_condition_list.append(planning_condition)
                    self.expanded_condition_dict[premise_condition] = planning_condition

                    # cost
                    new_cost = cost + action.cost
                    premise_condition_cost_list.append(CondCostPair(premise_condition,new_cost))

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

        # cost
        return premise_condition_cost_list

class MAOBTP(MABTP):
    def __init__(self,verbose=False,start = None):
        self.planned_agent_list = None
        self.verbose = verbose
        self.start = start

    def bfs_planning(self, goal, action_lists):
        planning_agent_list = []
        for id,action_list in enumerate(action_lists):
            planning_agent_list.append(BfsPlanningAgent(action_list,goal,id,self.verbose,start=self.start))

        goal_cost = CondCostPair(goal,0)
        explored_condition_list=[]
        heapq.heappush(explored_condition_list, goal_cost)


        while explored_condition_list != []:

            condition_cost = heapq.heappop(explored_condition_list)
            condition,cost = condition_cost.cond,condition_cost.cost

            if self.verbose: print_colored(f"C:{condition}","green")
            for agent in planning_agent_list:
                if self.verbose: print_colored(f"Agent:{agent.id}", "purple")
                premise_condition_cost_list = agent.one_step_expand(condition_cost)
                explored_condition_list += [condition_cost for condition_cost in premise_condition_cost_list]

            if self.start!=None and self.start<=condition:
                break

        self.planned_agent_list = planning_agent_list

    def output_bt_list(self,behavior_libs):
        bt_list = []
        for i,agent in enumerate(self.planned_agent_list):
            bt = agent.output_bt(behavior_libs[i])
            bt_list.append(bt)
        return bt_list

    def get_btml_list(self):
        btml_list = []
        for i,agent in enumerate(self.planned_agent_list):
            agent.create_btml()
            bt = agent.btml
            btml_list.append(bt)
        return btml_list