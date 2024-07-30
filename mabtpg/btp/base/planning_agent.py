from mabtpg.behavior_tree.behavior_tree import BehaviorTree
from mabtpg.utils import parse_predicate_logic
from mabtpg.utils.any_tree_node import AnyTreeNode
from mabtpg.behavior_tree.constants import NODE_TYPE
import re
import mabtpg
from mabtpg.utils.tools import print_colored
from mabtpg.behavior_tree import BTML
from mabtpg.btp.base.planning_condition import PlanningCondition

class PlanningAgent:
    def __init__(self,action_list,goal,id=None,verbose=False,start = None):
        self.id = id
        self.action_list = action_list
        self.expanded_condition_dict = {}
        self.goal = goal
        self.goal_condition = PlanningCondition(goal)
        self.expanded_condition_dict[goal] = self.goal_condition

        self.verbose = verbose

        self.start = start # ???delete

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

    def check_conflict(self, premise_condition):
        near_state_dic = {}
        holding_state_dic = {}
        empty_hand_dic = {}
        room_state_dic = {}
        toggle_state_dic={}

        for c in premise_condition:
            # 检测 IsNear 模式
            match_near = re.search(r'IsNear\(([^)]+)\)', c)
            if match_near:
                content = match_near.group(1)
                elements = content.split(',')
                agent_id = elements[0].strip()
                obj_id = elements[1].strip()
                if agent_id in near_state_dic:
                    if near_state_dic[agent_id] != obj_id:
                        if self.verbose:
                            print(
                                f"Conflict detected: {agent_id} is near more than one object: {near_state_dic[agent_id]} and {obj_id}.")
                        return True
                else:
                    near_state_dic[agent_id] = obj_id

            # 检测 IsHolding 模式
            match_holding = re.search(r'IsHolding\(([^)]+)\)', c)
            if match_holding:
                content = match_holding.group(1)
                elements = content.split(',')
                agent_id = elements[0].strip()
                obj_id = elements[1].strip()
                if agent_id in holding_state_dic:
                    if holding_state_dic[agent_id] != obj_id:
                        if self.verbose:
                            print(
                                f"Conflict detected: {agent_id} is holding more than one object: {holding_state_dic[agent_id]} and {obj_id}.")
                        return True
                elif agent_id in empty_hand_dic:
                    if self.verbose:
                        print(f"Conflict detected: {agent_id} is reported both holding {obj_id} and having an empty hand.")
                    return True
                else:
                    holding_state_dic[agent_id] = obj_id

            # 检测 IsHandEmpty 模式
            match_empty = re.search(r'IsHandEmpty\(([^)]+)\)', c)
            if match_empty:
                agent_id = match_empty.group(1).strip()
                if agent_id in holding_state_dic:
                    if self.verbose:
                        print(
                            f"Conflict detected: {agent_id} is reported both having an empty hand and holding {holding_state_dic[agent_id]}.")
                    return True
                empty_hand_dic[agent_id] = True

            # 检测 IsInRoom 模式
            match_room = re.search(r'IsInRoom\(([^,]+),(\d+)\)', c)
            if match_room:
                entity_id = match_room.group(1).strip()
                room_id = match_room.group(2).strip()
                if entity_id in room_state_dic:
                    if room_state_dic[entity_id] != room_id:
                        if self.verbose:
                            print(f"Conflict detected: {entity_id} is reported in more than one room: {room_state_dic[entity_id]} and {room_id}.")
                        return True
                else:
                    room_state_dic[entity_id] = room_id


            # 检查 IsOpen() 和 IsClose() 不能针对同一个物体都有
            # 检测 IsOpen 和 IsClose 模式
            match_open = re.search(r'IsOpen\(([^)]+)\)', c)
            match_close = re.search(r'IsClose\(([^)]+)\)', c)

            if match_open:
                obj_id = match_open.group(1).strip()
                if obj_id in toggle_state_dic and toggle_state_dic[obj_id] == 'close':
                    if self.verbose:
                        print(f"Conflict detected: {obj_id} is reported both open and close.")
                    return True
                toggle_state_dic[obj_id] = 'open'
            if match_close:
                obj_id = match_close.group(1).strip()
                if obj_id in toggle_state_dic and toggle_state_dic[obj_id] == 'open':
                    if self.verbose:
                        print(f"Conflict detected: {obj_id} is reported both open and close.")
                    return True
                toggle_state_dic[obj_id] = 'close'

        return False


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
                cls_name, args = parse_predicate_logic(current_condition.action)
                # args = tuple(list(args) + [current_condition.action_pre])
                action_node = AnyTreeNode(NODE_TYPE.action,cls_name,args)

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

                #### Finish task action
                seq_task_parent.add_child(AnyTreeNode(NODE_TYPE.action,"FinishTask"))
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
                # if current_condition.children == [] and len(current_condition.condition_set) == 0:
                #     current_condition.parent.add_child(action_node)
                # else:
                sequence_node.add_child(action_node)
                current_condition.parent.add_child(sel_comp_parent)

                sel_comp_parent.add_child(sequence_node)


        self.anytree_root = anytree_root



    # def create_anytree(self):
    #     anytree_root = AnyTreeNode(NODE_TYPE.selector)
    #     stack = []
    #     # add goal conditions into root
    #     self.add_conditions(self.goal_condition,anytree_root)
    #     for children in self.goal_condition.children:
    #         children.parent = anytree_root
    #         stack.append(children)
    #
    #     while stack != []:
    #         current_condition = stack.pop(0)
    #
    #         # create a sequence node and its condition-action pair
    #         sequence_node = AnyTreeNode(NODE_TYPE.sequence)
    #         if current_condition.children == []:
    #             condition_parent = sequence_node
    #         else:
    #             condition_parent = AnyTreeNode(NODE_TYPE.selector)
    #             sequence_node.add_child(condition_parent)
    #             # add children into stack
    #             for children in current_condition.children:
    #                 children.parent = condition_parent
    #                 stack.append(children)
    #         # add condition
    #         self.add_conditions(current_condition,condition_parent)
    #         # add action
    #         cls_name, args = parse_predicate_logic(current_condition.action)
    #         action_node = AnyTreeNode(NODE_TYPE.action,cls_name,args)
    #
    #         # add the sequence node into its parent
    #         if current_condition.children == [] and len(current_condition.condition_set) == 0:
    #             current_condition.parent.add_child(action_node)
    #         else:
    #             sequence_node.add_child(action_node)
    #             current_condition.parent.add_child(sequence_node)
    #
    #     self.anytree_root = anytree_root

    def create_btml(self):
        self.create_anytree()
        btml = BTML()
        btml.anytree_root = self.anytree_root

        self.btml = btml

    def output_bt(self,behavior_lib=None):
        self.create_btml()

        bt = BehaviorTree(btml=self.btml, behavior_lib=behavior_lib)

        return bt

    def add_conditions(self,planning_condition,parent):
        condition_set = planning_condition.condition_set
        if len(condition_set) == 0: return

        if len(condition_set) == 1:
            cls_name, args = parse_predicate_logic(list(condition_set)[0])
            parent.add_child(AnyTreeNode(NODE_TYPE.condition,cls_name,args))
        else:
            sequence_node = AnyTreeNode(NODE_TYPE.sequence)
            for condition_node_name in condition_set:
                cls_name, args = parse_predicate_logic(condition_node_name)
                sequence_node.add_child(AnyTreeNode(NODE_TYPE.condition,cls_name,args))

            sub_btml = BTML()
            sub_btml.anytree_root = sequence_node

            composite_condition = AnyTreeNode("composite_condition",cls_name=None, info={'sub_btml':sub_btml})

            parent.add_child(composite_condition)


    def planning(self):
        explored_condition_list = [self.goal]

        while explored_condition_list != []:
            condition = explored_condition_list.pop(0)
            if self.verbose: print_colored(f"C:{condition}","green")
            premise_condition_list = self.one_step_expand(condition)
            explored_condition_list += [planning_condition.condition_set for planning_condition in premise_condition_list]

