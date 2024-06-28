
from mabtpg.behavior_tree.behavior_tree import BehaviorTree
from mabtpg.utils import parse_predicate_logic
from mabtpg.utils.any_tree_node import AnyTreeNode
from mabtpg.behavior_tree.constants import NODE_TYPE

import mabtpg



class PlanningCondition:
    def __init__(self,condition,action=None):
        self.condition_set = condition
        self.action = action
        self.children = []
        # for generate bt
        self.parent_node = None

class PlanningAgent:
    def __init__(self,action_list,goal):
        self.action_list = action_list
        self.expanded_condition_dict = {}
        self.goal_condition = PlanningCondition(goal)
        self.expanded_condition_dict[goal] = self.goal_condition

    def one_step_expand(self, condition):
        # find premise conditions
        premise_condition_list = []
        for action in self.action_list:
            if self.is_consequence(condition,action):
                premise_condition = frozenset((action.pre | condition) - action.add)
                if self.has_no_subset(premise_condition):
                    planning_condition = PlanningCondition(premise_condition,action.name)
                    premise_condition_list.append(planning_condition)
                    self.expanded_condition_dict[premise_condition] = planning_condition

        # insert premise conditions into BT
        inside_condition = self.expanded_condition_dict.get(condition,None)
        if inside_condition:
            self.inside_expand(inside_condition, premise_condition_list)
        else:
            self.outside_expand(premise_condition_list)

        return premise_condition_list

    # check if `condition` is the consequence of `action`
    def is_consequence(self,condition,action):
        if condition & ((action.pre | action.add) - action.del_set) <= set():
            return False
        if (condition - action.del_set) != condition:
            return False
        return True

    def has_no_subset(self, condition):
        for expanded_condition in self.expanded_condition_dict:
            if expanded_condition <= condition:
                return False
        return True

    def inside_expand(self,inside_condition, premise_condition_list):
        inside_condition.children += premise_condition_list

    def outside_expand(self,premise_condition_list):
        self.goal_condition.children += premise_condition_list

    def output_bt(self,behavior_lib=None):
        anytree_root = AnyTreeNode(NODE_TYPE.selector)
        stack = []
        # add goal conditions into root
        self.add_conditions(self.goal_condition,anytree_root)
        for children in self.goal_condition.children:
            children.parent = anytree_root
            stack.append(children)

        while stack != []:
            current_condition = stack.pop()

            # create a sequence node and its condition-action pair
            sequence_node = AnyTreeNode(NODE_TYPE.sequence)
            if current_condition.children == []:
                condition_parent = sequence_node
            else:
                condition_parent = AnyTreeNode(NODE_TYPE.condition)
                sequence_node.add_child(condition_parent)
                # add children into stack
                for children in current_condition.children:
                    children.parent = condition_parent
                    stack.append(children)
            # add condition
            self.add_conditions(current_condition,condition_parent)
            # add action
            cls_name, args = parse_predicate_logic(current_condition.action)
            sequence_node.add_child(AnyTreeNode(NODE_TYPE.action,cls_name,args))

            # add the sequence node into its parent
            current_condition.parent.add_child(sequence_node)

        bt = BehaviorTree(anytree=anytree_root,behavior_lib=behavior_lib)

        return bt


    def add_conditions(self,planning_condition,parent):
        for condition_node_name in planning_condition.condition_set:
            cls_name, args = parse_predicate_logic(condition_node_name)
            parent.add_child(AnyTreeNode(NODE_TYPE.condition,cls_name,args))

class MABTP:
    def __init__(self):
        self.planned_agent_list = None

    def planning(self, goal, action_lists):
        planning_agent_list = []
        for action_list in action_lists:
            planning_agent_list.append(PlanningAgent(action_list,goal))

        explored_condition_list = [goal]

        while explored_condition_list != []:
            condition = explored_condition_list.pop()
            for agent in planning_agent_list:
                premise_condition_list = agent.one_step_expand(condition)
                explored_condition_list += [planning_condition.condition_set for planning_condition in premise_condition_list]

        self.planned_agent_list = planning_agent_list


    def output_bt_list(self,behavior_libs):
        bt_list = []
        for i,agent in enumerate(self.planned_agent_list):
            bt = agent.output_bt(behavior_libs[i])
            bt_list.append(bt)
        return bt_list