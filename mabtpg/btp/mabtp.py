
from mabtpg.behavior_tree.behavior_tree import BehaviorTree
from mabtpg.utils import parse_predicate_logic
from mabtpg.utils.any_tree_node import AnyTreeNode
from mabtpg.behavior_tree.constants import NODE_TYPE
import re
import mabtpg
from mabtpg.utils.tools import print_colored
from mabtpg.behavior_tree import BTML
from mabtpg.btp.base.planning_agent import PlanningAgent
import time


class MABTP:
    def __init__(self,verbose=False,start = None,env=None):
        self.planned_agent_list = None
        self.verbose = verbose
        self.start = start

        self.record_expanded_num = 0
        self.env = env

        self.expanded_time=0


    def planning(self, goal, action_lists):

        start_time = time.time()

        planning_agent_list = []
        for id,action_list in enumerate(action_lists):
            planning_agent_list.append(PlanningAgent(action_list,goal,id,self.verbose,start=self.start,env=self.env))

        explored_condition_list = [goal]

        while explored_condition_list != []:

            self.record_expanded_num+=1

            condition = explored_condition_list.pop(0)
            if self.verbose: print_colored(f"C:{condition}","green")
            for agent in planning_agent_list:
                if self.verbose: print_colored(f"Agent:{agent.id}", "purple")
                print_colored(f"Agent:{agent.id}", "purple")
                premise_condition_list = agent.one_step_expand(condition)
                explored_condition_list += [planning_condition.condition_set for planning_condition in premise_condition_list]

            if self.start!=None and self.start>=condition:
                break

            if time.time() - start_time> 20:
                self.expanded_time = time.time() - start_time
                break

        self.planned_agent_list = planning_agent_list

    def bfs_planning(self, goal, action_lists):
        planning_agent_list = []
        for id,action_list in enumerate(action_lists):
            planning_agent_list.append(PlanningAgent(action_list,goal,id,self.verbose,start=self.start,env=self.env))

        explored_condition_list = [goal]

        while explored_condition_list != []:
            condition_cost = explored_condition_list.pop(0)
            condition = condition_cost[0]

            if self.verbose: print_colored(f"C:{condition}","green")
            for agent in planning_agent_list:
                if self.verbose: print_colored(f"Agent:{agent.id}", "purple")
                print_colored(f"Agent:{agent.id}", "purple")
                premise_condition_list = agent.one_step_expand(condition)
                explored_condition_list += [planning_condition.condition_set for planning_condition in premise_condition_list]

            if self.start!=None and self.start>=condition:
                break

        self.planned_agent_list = planning_agent_list

    def output_bt_list(self,behavior_libs):
        bt_list = []
        for i,agent in enumerate(self.planned_agent_list):
            bt = agent.output_bt(behavior_libs[i])
            bt_list.append(bt)
        return bt_list


    def new_output_pruned_bt_list(self,behavior_libs):
        bt_list = []
        for i,agent in enumerate(self.planned_agent_list):
            bt = agent.new_output_pruned_bt(behavior_libs[i])
            bt_list.append(bt)
        return bt_list


    def get_btml_list(self):
        btml_list = []
        for i,agent in enumerate(self.planned_agent_list):
            agent.create_btml()
            bt = agent.btml
            btml_list.append(bt)
        return btml_list