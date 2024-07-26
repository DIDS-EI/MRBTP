
from mabtpg.behavior_tree.behavior_tree import BehaviorTree
from mabtpg.utils import parse_predicate_logic
from mabtpg.utils.any_tree_node import AnyTreeNode
from mabtpg.behavior_tree.constants import NODE_TYPE
import re
import mabtpg
from mabtpg.utils.tools import print_colored
from mabtpg.behavior_tree import BTML
from mabtpg.btp.base.planning_agent import PlanningAgent
from mabtpg.btp.base.planning_condition import PlanningCondition
from mabtpg.btp.mabtp import MABTP
from default_bt_tools import *

class PlanningAgentTest(PlanningAgent):
    def __init__(self, action_list, goal, id=None, verbose=False, start=None):
        super().__init__(action_list, goal, id, verbose, start)
        self.default_bt = None

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
                    print("action:",action)
                    planning_condition = PlanningCondition(premise_condition,action)  # action, not action's name
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

    def check_conflict(self, premise_condition):
        return False

    def add_conditions(self,planning_condition,parent):
        condition_set = planning_condition.condition_set
        if len(condition_set) == 0: return

        if len(condition_set) == 1:
            # cls_name, args = parse_predicate_logic(list(condition_set)[0])
            parent.add_child(AnyTreeNode(NODE_TYPE.condition,"NumCondition",str(condition_set[0])))
        else:
            sequence_node = AnyTreeNode(NODE_TYPE.sequence)
            for condition_node_name in condition_set:
                # cls_name, args = parse_predicate_logic(condition_node_name)
                sequence_node.add_child(AnyTreeNode(NODE_TYPE.condition,"NumCondition",str(condition_node_name)))

            sub_btml = BTML()
            sub_btml.anytree_root = sequence_node

            composite_condition = AnyTreeNode("composite_condition",cls_name=None, info={'sub_btml':sub_btml})

            parent.add_child(composite_condition)


    def create_btml(self):
        self.create_anytree()
        btml = BTML()
        btml.anytree_root = self.anytree_root

        self.btml = btml


    def create_anytree(self):

        task_num=0

        anytree_root = AnyTreeNode(NODE_TYPE.selector)
        stack = []
        # add goal conditions into root
        self.add_conditions(self.goal_condition,anytree_root)
        for children in self.goal_condition.children:
            children.parent = anytree_root
            stack.append(children)

        while stack != []:
            current_condition = stack.pop(0)

            if current_condition.composition_action_flag == False:
                # create a sequence node and its condition-action pair
                sequence_node = AnyTreeNode(NODE_TYPE.sequence)
                if current_condition.children == []:
                    condition_parent = sequence_node
                else:
                    condition_parent = AnyTreeNode(NODE_TYPE.selector)
                    sequence_node.add_child(condition_parent)
                    # add children into stack
                    for children in current_condition.children:
                        children.parent = condition_parent
                        stack.append(children)
                # add condition
                self.add_conditions(current_condition,condition_parent)
                # add action
                # cls_name, args = parse_predicate_logic(current_condition.action)
                # args = tuple(list(args) + [current_condition.action_pre])
                action_node = AnyTreeNode(NODE_TYPE.action,"NumAction",[current_condition.action],has_args=False)

                # add the sequence node into its parent
                if current_condition.children == [] and len(current_condition.condition_set) == 0:
                    current_condition.parent.add_child(action_node)
                else:
                    sequence_node.add_child(action_node)
                    current_condition.parent.add_child(sequence_node)

            # for composition_action
            # elif current_condition.composition_action_flag == True:
            else:

                sel_comp_parent = AnyTreeNode(NODE_TYPE.selector)

                seq_task_parent = AnyTreeNode(NODE_TYPE.sequence)

                # task_flag_condition = AnyTreeNode(NODE_TYPE.condition, "IsSelfTask",
                #                                   ([current_condition.sub_goal]))
                task_flag_condition = AnyTreeNode(NODE_TYPE.condition,"IsSelfTask",([task_num,current_condition.sub_goal]))
                cls_name, args = parse_predicate_logic(current_condition.action)
                # args = tuple(list(args) + [current_condition.action_pre])
                task_comp_action = AnyTreeNode(NODE_TYPE.action,cls_name,args)
                # seq add two children
                seq_task_parent.add_child(task_flag_condition)
                seq_task_parent.add_child(task_comp_action)
                sel_comp_parent.add_child(seq_task_parent)

                sequence_node = AnyTreeNode(NODE_TYPE.sequence)
                if current_condition.children == []:
                    condition_parent = sequence_node
                else:
                    condition_parent = AnyTreeNode(NODE_TYPE.selector)
                    sequence_node.add_child(condition_parent)
                    # add children into stack
                    for children in current_condition.children:
                        children.parent = condition_parent
                        stack.append(children)
                # add condition
                self.add_conditions(current_condition,condition_parent)
                # add action
                # print("current_condition.sub_goal:",current_condition.sub_goal)
                # action_node = AnyTreeNode(NODE_TYPE.action,"SelfAcceptTask",(task_num,current_condition.sub_goal,current_condition.dependency))

                # action_node = AnyTreeNode(NODE_TYPE.action, "SelfAcceptTask", [current_condition.sub_goal])
                action_node = AnyTreeNode(NODE_TYPE.action,"SelfAcceptTask",(task_num,current_condition.sub_goal))
                task_num += 1
                # add the sequence node into its parent
                if current_condition.children == [] and len(current_condition.condition_set) == 0:
                    current_condition.parent.add_child(action_node)
                else:
                    sequence_node.add_child(action_node)
                    current_condition.parent.add_child(sel_comp_parent)

                sel_comp_parent.add_child(sequence_node)


        self.anytree_root = anytree_root




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


