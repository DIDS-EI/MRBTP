
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
from default_bt_tools import *

class PlanningAgentTest(PlanningAgent):
    def __init__(self, action_list, goal, id=None, verbose=False, start=None):
        super().__init__(action_list, goal, id, verbose, start)
        self.default_bt = None

    def check_conflict(self, premise_condition):
        return False

    def add_conditions(self, condition_set, parent_node):
        for cond in condition_set:
            cond_node = Leaf(type='cond', content=cond)
            parent_node.add_child([cond_node])

    def create_default_bt(self):
        task_num = 0

        # Create the root node of the behavior tree
        self.default_bt = ControlBT(type='?')

        # Add goal conditions to the root
        goal_node = Leaf(type='cond', content=self.goal_condition.condition_set)
        self.default_bt.add_child([goal_node])

        stack = [(self.goal_condition, self.default_bt)]
        while stack:
            current_condition, parent_node = stack.pop(0)

            if not current_condition.composition_action_flag:
                # Create a sequence node and its condition-action pair
                sequence_node = ControlBT(type='>')

                if not current_condition.children:
                    condition_parent = sequence_node
                else:
                    condition_parent = ControlBT(type='?')
                    sequence_node.add_child([condition_parent])

                    for child in current_condition.children:
                        stack.append((child, condition_parent))

                # Add condition
                self.add_conditions(current_condition.condition_set, condition_parent)

                # Add action
                action_node = Leaf(type='act', content=current_condition.action)
                sequence_node.add_child([action_node])

                # Add the sequence node to its parent
                parent_node.add_child([sequence_node])

            else:
                # Handle composition actions
                sel_comp_parent = ControlBT(type='?')
                seq_task_parent = ControlBT(type='>')

                task_flag_condition = Leaf(type='cond', content="IsSelfTask")
                task_flag_condition.content = ([task_num, current_condition.sub_goal])
                task_comp_action = Leaf(type='act', content=current_condition.action)

                seq_task_parent.add_child([task_flag_condition, task_comp_action])
                sel_comp_parent.add_child([seq_task_parent])

                sequence_node = ControlBT(type='>')

                if not current_condition.children:
                    condition_parent = sequence_node
                else:
                    condition_parent = ControlBT(type='?')
                    sequence_node.add_child([condition_parent])

                    for child in current_condition.children:
                        stack.append((child, condition_parent))

                self.add_conditions(current_condition.condition_set, condition_parent)

                action_node = Leaf(type='act', content="SelfAcceptTask")
                action_node.content = (task_num, current_condition.sub_goal)
                task_num += 1

                # Add the sequence node to its parent
                parent_node.add_child([sel_comp_parent])
                sel_comp_parent.add_child([sequence_node])

        # self.default_bt.print_nodes()




class MABTP_test(MABTP):
    def __init__(self,verbose=False,start = None):
        super(MABTP_test,self).__init__(verbose,start)

    def planning(self, goal, action_lists):
        planning_agent_list = []
        for id,action_list in enumerate(action_lists):
            planning_agent_list.append(PlanningAgentTest(action_list,goal,id,self.verbose,start=self.start))

        explored_condition_list = [goal]

        while explored_condition_list != []:
            condition = explored_condition_list.pop(0)
            if self.verbose: print_colored(f"C:{condition}","green")
            for agent in planning_agent_list:
                if self.verbose: print_colored(f"Agent:{agent.id}", "purple")
                premise_condition_list = agent.one_step_expand(condition)
                explored_condition_list += [planning_condition.condition_set for planning_condition in premise_condition_list]

            if self.start!=None and self.start<=condition:
                break

        self.planned_agent_list = planning_agent_list



    def create_default_bt(self):
        default_bt_ls = []
        for i,agent in enumerate(self.planned_agent_list):
            agent.create_default_bt()
            bt = agent.default_bt
            default_bt_ls.append(bt)
        return default_bt_ls
