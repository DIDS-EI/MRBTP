import random
import string
import networkx as nx
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.envs.numerical_env.numerical_env.numsim_tools import frozenset_to_str,convert_cstr_set_to_num_set
from mabtpg.utils.tools import print_colored
import numpy as np

random.seed(0)
np.random.seed(0)


class DataGenerator:
    def __init__(self, num_elements=10, total_elements_set=None, max_depth=2, max_branch=5,need_split_action=False, num_agent=2):
        self.num_elements = num_elements
        if total_elements_set == None:
            self.total_elements_set = frozenset(f"C({i})" for i in range(num_elements))
            # self.total_elements_set = frozenset(range(num_elements))
        else:
            self.total_elements_set = frozenset(total_elements_set)
        self.max_depth = max_depth
        self.max_branch = max_branch
        self.need_split_action = need_split_action

        self.num_agent = num_agent

    def get_parts_from_state(self, state):
        part_num = random.randint(1, min(self.max_branch,len(state))) # 划分成几部分
        state_list = list(state)
        random.shuffle(state_list)

        parts = [set() for _ in range(part_num)]
        for i, element in enumerate(state_list):
            parts[i % part_num].add(element)

        non_empty_parts = [part for part in parts if part]
        empty_parts_count = part_num - len(non_empty_parts)

        if empty_parts_count > 0:
            for _ in range(empty_parts_count):
                random_part = random.choice(non_empty_parts)
                element_to_move = random_part.pop()
                empty_part = next(part for part in parts if not part)
                empty_part.add(element_to_move)
                if random_part:
                    non_empty_parts.append(random_part)
        # print_colored(f"State Split {state} into {parts}", color='orange')
        return parts

    def generate_random_state(self):
        num = random.randint(min(self.num_elements, 5), self.num_elements)
        return frozenset(random.sample(self.total_elements_set, num))

    def generate_random_goal(self,range_num=None,range_elements=None):
        if range_num==None:
            num_goal = random.randint(min(self.num_elements, 1), int(self.num_elements / 2))
            return frozenset(random.sample(self.total_elements_set, num_goal))
        else:
            num_goal = random.randint(min(range_elements, 1), range_elements)
            total_elements_set = frozenset(f"C({i})" for i in range(range_num*range_elements,(range_num+1)*range_elements))
            return frozenset(random.sample(total_elements_set, num_goal))

    def generate_dataset(self):

        # range_num=0
        # range_elements = self.num_elements
        range_num=None
        range_elements=self.num_elements

        goal = self.generate_random_goal(range_num,range_elements)
        # range_num +=1

        start = set()
        actions = []
        leaves = [(goal, 0)]
        node_index = 0
        nodes = {node_index: goal}
        edges = []
        node_index += 1
        action_index = 0

        while leaves:
            current_leaves = []
            for leaf, depth in leaves:
                if depth >= self.max_depth:
                    continue

                if leaf != set():
                    parts = self.get_parts_from_state(leaf)
                else:
                    parts=[]
                for part in parts:
                    # if random.random()>0.5 or len(actions)<=1:
                    new_state, action,range_num = self.generate_start_and_action(leaf, part, goal,range_num,range_elements)
                    # range_num+=1

                    action.name = self.generate_action_name(depth, action_index, action.pre, action.add, action.del_set)
                    action_index += 1

                    action.add_part = part
                    actions.append(action)
                    current_leaves.append((new_state, depth + 1))

                    nodes[node_index] = new_state
                    edges.append((list(nodes.keys())[list(nodes.values()).index(leaf)], node_index,
                                  action.name + "_" + str(action.add_part) + "\n pre_" + str(set(action.pre))))
                    node_index += 1

            if not current_leaves:
                for leaf, _ in leaves:
                    start |= leaf
            leaves = current_leaves

        for leaf, _ in leaves:
            start |= leaf

        start = frozenset(start)
        dataset = {
            'goal': goal,
            'goal_num': convert_cstr_set_to_num_set(goal),
            'start': start,
            'start_num': convert_cstr_set_to_num_set(start),
            'nodes': nodes,
            'edges': edges,
            'comp_btml_ls': {},
            'actions_with_cmp':[],
            'actions_without_cmp':[],

            "CABTP_expanded_num":0
        }

        # cut composition to sub actions
        if self.need_split_action:
            (dataset['actions_with_cmp'], dataset['actions_without_cmp'],
             dataset['comp_btml_ls'],dataset['CABTP_expanded_num']) = \
                self.split_actions_and_plan_sub_btml(actions)

        return dataset

    def split_actions_and_plan_sub_btml(self, actions):
        """
        Split composite actions into sub-actions and generate corresponding BTML structures.

        Args:
        - dataset: The original dataset containing actions.
        - data_generator: The object used to generate split actions.

        Returns:
        - new_actions: The list of new actions after splitting.
        - comp_btml_ls: A dictionary of BTML structures for each composite action.
        """
        def generate_composition_action_name(original_name):
            import re
            # input_string = "A(12,34,56,78,90)"
            # 使用正则表达式匹配括号内的内容
            match = re.search(r'\(([^)]+)\)', original_name)
            first_value=-1
            if match:
                # 提取第一个逗号分隔的部分
                content = match.group(1)
                first_value = content.split(',')[0]
                index, depth = first_value.split('_')
            return f"CMP_A{index}_D{depth}"

        split_actions_dict = {}
        new_actions_with_cmp = list(actions)
        new_actions_without_cmp = list(actions)
        for action in actions:
            # print_colored(f"act:{action.name} pre:{action.pre} add:{action.add} del:{action.del_set}",color='blue')
            if len(action.add) >= 3:
                if random.random() < 0.8:
                    split_action_ls = self.split_action_to_sub_actions(action, min_splits=2, max_splits=6)
                    print_colored(f"Act Split :{action.name} pre:{action.pre} add:{action.add} del:{action.del_set}", color='blue')

                    # without_cmp
                    new_actions_without_cmp.remove(action)
                    new_actions_without_cmp.extend(split_action_ls)

                    # with_cmp
                    new_actions_with_cmp.extend(split_action_ls)
                    split_actions_dict[action] = split_action_ls
                    action.name = generate_composition_action_name(action.name)
                    action.cost = 0

        # 将每个组合动作的 btml 保存起来
        # 得到一个 comp_act_BTML_dic[action.name] = sub_btml
        from num_cabtp import Num_CABTP
        from mabtpg.behavior_tree.btml.BTML import BTML
        comp_actions_BTML_dic = {}
        CABTP_expanded_num = 0
        for comp_act, split_action_ls in split_actions_dict.items():
            sub_goal = frozenset((comp_act.pre | comp_act.add) - comp_act.del_set)
            planning_algorithm = Num_CABTP(verbose=False, goal=sub_goal, sequence=split_action_ls,
                                           action_list=split_action_ls)
            planning_algorithm.planning()
            CABTP_expanded_num+= planning_algorithm.record_expanded_num

            planning_algorithm.create_anytree()

            sub_btml = BTML()
            sub_btml.cls_name = comp_act.name
            sub_btml.anytree_root = planning_algorithm.anytree_root

            comp_actions_BTML_dic[comp_act.name] = sub_btml
        return new_actions_with_cmp, new_actions_without_cmp, comp_actions_BTML_dic,CABTP_expanded_num

    def generate_start_and_action(self, parent_leaf, part, goal,range_num=None,range_elements=None):
        action = PlanningAction()
        action.add = part

        if range_num ==None:
            pre_size = random.randint(0, len(self.total_elements_set) - len(goal))
            action.pre = set(random.sample(self.total_elements_set - goal, pre_size))

            del_size = random.randint(0, len(self.total_elements_set) - len(parent_leaf))
            action.del_set = set(random.sample(self.total_elements_set - parent_leaf, del_size))

            start = (parent_leaf - action.add) | action.pre
        else:
            total_elements_set =  frozenset(f"C({i})" for i in range(range_num*self.num_elements,(range_num+1)*self.num_elements))
            pre_size = random.randint(1, int(len(total_elements_set)/2))
            action.pre = set(random.sample(total_elements_set - goal, pre_size))

            range_num += 1
            del_total_elements_set = frozenset( f"C({i})" for i in range(range_num * self.num_elements, (range_num + 1) * self.num_elements))
            del_size = random.randint(0, int(len(del_total_elements_set)-pre_size))
            action.del_set = set(random.sample(del_total_elements_set - action.pre-parent_leaf, del_size))

            # start = (parent_leaf - action.add) | action.pre
            action.pre = frozenset(action.pre - action.add)
            action.add = frozenset(action.add)
            action.del_set = frozenset(action.del_set - part)
            start = action.pre

        action.pre = frozenset(action.pre - action.add)
        action.add = frozenset(action.add)
        action.del_set = frozenset(action.del_set - part)


        return frozenset(start), action, range_num

    def save_tree_as_dot(self, dataset, filename):
        G = nx.DiGraph()
        nodes = dataset['nodes']
        edges = dataset['edges']

        for node, state in nodes.items():
            G.add_node(node, label=str(state))

        for edge in edges:
            parent, child, action_name = edge
            G.add_edge(child, parent, label=action_name)

        nx.drawing.nx_pydot.write_dot(G, filename)

    @staticmethod
    def generate_predicates(num_pred):
        predicates = []
        for i in range(num_pred):
            if i < 26:
                predicates.append(string.ascii_lowercase[i])
            else:
                first = (i // 26) - 1
                second = i % 26
                predicates.append(string.ascii_lowercase[first] + string.ascii_lowercase[second])
        return predicates

    def generate_action_name(self, depth, index, pre,add, del_set):
        pre_str = frozenset_to_str(pre)
        add_str = frozenset_to_str(add)
        del_set_str = frozenset_to_str(del_set)

        return f"A({index}_{depth},{pre_str},{add_str},{del_set_str})"

    def split_action_to_sub_actions(self, action, min_splits=2, max_splits=4):
        def generate_split_action_name(parent_name, index,pre,add, del_set):
            import re
            # input_string = "A(12,34,56,78,90)"
            # 使用正则表达式匹配括号内的内容
            match = re.search(r'\(([^)]+)\)', parent_name)
            first_value=-1
            if match:
                # 提取第一个逗号分隔的部分
                content = match.group(1)
                first_value = content.split(',')[0]
            pre_str = frozenset_to_str(pre)
            add_str = frozenset_to_str(add)
            del_set_str = frozenset_to_str(del_set)
            return f"A({first_value}_{index},{pre_str},{add_str},{del_set_str})"

        add_elements = list(action.add)
        num_splits = random.randint(min_splits, min(len(add_elements), max_splits))
        random.shuffle(add_elements)

        split_actions = []
        current_pre = action.pre
        remaining_add = set(action.add)
        remaining_del = set(action.del_set)

        # Ensure the last split gets whatever remains
        for i in range(num_splits):
            if i == num_splits - 1:
                new_add = remaining_add
                new_del = remaining_del
            else:
                num_add_to_take = max(1, len(remaining_add) // (num_splits - i))
                new_add = set(random.sample(list(remaining_add), num_add_to_take))
                remaining_add -= new_add

                num_del_to_take = max(1, len(remaining_del) // (num_splits - i))
                if len(remaining_del) == 0:
                    new_del = set()
                else:
                    new_del = set(random.sample(list(remaining_del), num_del_to_take))
                remaining_del -= new_del

            new_name = generate_split_action_name(action.name, i,frozenset(current_pre), frozenset(new_add), frozenset(new_del))

            # new_action = PlanningAction(new_name, current_pre, new_add, new_del,cost=0)
            new_action = PlanningAction(new_name, frozenset(current_pre), frozenset(new_add), frozenset(new_del))
            current_pre = new_add

            split_actions.append(new_action)

        return split_actions

    def assign_actions_to_agents(self, dataset, num_agent=None,with_comp_action=True):
        """
        Assign actions to agents.

        Args:
        - dataset: The dataset containing actions.
        - num_agent: The number of agents.

        Returns:
        - agent_actions: A list of lists, where each sublist contains actions assigned to an agent.
        """
        if num_agent != None:
            self.num_agent = num_agent
        if with_comp_action==True:
            datasets_actions = dataset["actions_with_cmp"]
        else:
            datasets_actions = dataset["actions_without_cmp"]

        # Allocate actions to each agent
        agents_actions = [[] for _ in range(self.num_agent)]
        for action in datasets_actions:
            # Randomly choose at least one agent
            num_assignments = random.randint(1, num_agent)
            assigned_agents = random.sample(range(num_agent), num_assignments)
            for agent_index in assigned_agents:
                agents_actions[agent_index].append(action)

        # Check if each agent has at least one action; if not, randomly assign one
        for i in range(num_agent):
            if not agents_actions[i]:  # If the agent has no actions assigned
                # Randomly choose an action to assign to this agent
                action_to_assign = random.choice(datasets_actions)
                agents_actions[i].append(action_to_assign)

        # Print the allocation result to see the action list of each agent
        for i, actions in enumerate(agents_actions):
            print(f"Agent {i + 1} actions:")
            for action in actions:
                print(f"  act:{action.name} pre:{action.pre} add:{action.add} del:{action.del_set}")

        dataset["agents_actions"] = agents_actions

        return agents_actions


# Usage example
num_data = 1
num_elements = 10
max_depth = 3

data_generator = DataGenerator(num_elements=num_elements, max_depth=max_depth)
datasets = [data_generator.generate_dataset() for _ in range(num_data)]

for i, dataset in enumerate(datasets):
    data_generator.save_tree_as_dot(dataset, f'{i}_generated_tree.dot')
