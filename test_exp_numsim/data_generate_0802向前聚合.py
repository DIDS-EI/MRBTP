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
    def __init__(self, max_depth=3,max_leaves=5, max_branch=5,cmp_ratio=0.5,max_cmp_act_split=5,max_action_steps=5,need_split_action=False, num_agent=2):

        self.max_depth=max_depth
        self.max_leaves = max_leaves
        self.max_branch = max_branch
        self.cmp_ratio = cmp_ratio
        self.max_cmp_act_split = max_cmp_act_split
        self.max_action_steps = max_action_steps
        self.need_split_action = need_split_action

        self.num_agent = num_agent

        self.unique = 1


    def generate_dataset(self):
        random.seed(0)
        np.random.seed(0)

        num_leaves = self.max_leaves
        max_branch = self.max_branch

        leaves = [(frozenset(),0,i) for i in range(num_leaves)]  # 随机生成 num_leafs 个空集作为叶子节点
        leaf_num = num_leaves
        nodes = {}
        edges = []
        action_index = 1
        all_actions = []
        new_state = set()
        new_depth = -1

        # while new_depth < self.max_depth:
        while len(leaves)>1 and new_depth < self.max_depth:

            # 随机挑选不大于 max_branch 个叶子节点
            branch_size = random.randint(1,min(max_branch, len(leaves)))
            selected_leaves = random.sample(leaves, branch_size)

            new_state = set()
            new_depth=-1

            actions = []
            for leaf,depth,index in selected_leaves:
                new_state |= leaf
                # 更新 new_depth 为 selected_leaves 中的最大深度
                if depth > new_depth:
                    new_depth = depth
            # new_depth 加 1
            new_depth += 1

            cur_node_index_ls = [] # (index,action)

            for i, (leaf,depth,index) in enumerate(selected_leaves):
                action = PlanningAction(pre=leaf, add={f"C({self.unique})"}, del_set=set())
                act_step = random.randint(1,self.max_action_steps)
                action.name = self.generate_action_name(0, action_index, action.pre, action.add, action.del_set, act_step)
                action_index += 1
                self.unique += 1
                actions.append(action)

                if leaf == frozenset():
                    cur_node_index_ls.append((len(nodes),action))
                    nodes[len(nodes)] =  frozenset()
                elif leaf not in nodes.values():
                    nodes[len(nodes)] = leaf
                    leaf_index = list(nodes.keys())[list(nodes.values()).index(leaf)]
                    cur_node_index_ls.append((leaf_index,action))

            all_actions.extend(actions)

            for action in actions:
                new_state |= action.add
            new_state = frozenset(new_state)
            leaves = [leaf for leaf in leaves if leaf not in selected_leaves]
            leaves.append((new_state, new_depth,leaf_num))
            leaf_num+=1


            if new_state not in nodes.values():
                node_index = len(nodes)
                nodes[node_index] = new_state
            else:
                node_index = list(nodes.keys())[list(nodes.values()).index(new_state)]
            for leaf_index,action in cur_node_index_ls:
                edges.append((node_index,leaf_index, f"{action.name}"))


            if new_depth >= self.max_depth:
                break


        # goal = frozenset(leaves[0])  # 最终聚合的结点作为goal
        goal = frozenset(new_state)
        start = frozenset()

        dataset = {
            'goal': goal,
            "goal_depth":new_depth,
            'goal_num': convert_cstr_set_to_num_set(goal),
            'start': start,
            'start_num': convert_cstr_set_to_num_set(start),
            'nodes': nodes,
            'edges': edges,
            'comp_actions_BTML_dic': {},
            'actions_with_cmp': [],
            'actions_without_cmp': [],
            "CABTP_expanded_num": 0
        }

        # cut composition to sub actions
        if self.need_split_action:
            (dataset['actions_with_cmp'], dataset['actions_without_cmp'],
             dataset['comp_actions_BTML_dic'], dataset['CABTP_expanded_num']) = \
                self.split_actions_and_plan_sub_btml(all_actions)

        return dataset

    def split_actions_and_plan_sub_btml(self, actions):
        """
        Split composite actions into sub-actions and generate corresponding BTML structures.

        Args:
        - dataset: The original dataset containing actions.
        - data_generator: The object used to generate split actions.

        Returns:
        - new_actions: The list of new actions after splitting.
        - comp_actions_BTML_dic: A dictionary of BTML structures for each composite action.
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
            if random.random() < self.cmp_ratio:
                split_action_ls = self.split_action_to_sub_actions(action, min_splits=2, max_splits=self.max_cmp_act_split)
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

    def generate_action_name(self, depth, index, pre,add, del_set,act_step):
        pre_str = frozenset_to_str(pre)
        add_str = frozenset_to_str(add)
        del_set_str = frozenset_to_str(del_set)

        return f"A({index}_{depth},{pre_str},{add_str},{del_set_str},{act_step})"

    def split_action_to_sub_actions(self, action, min_splits=2, max_splits=5):
        def generate_split_action_name(parent_name, index,pre,add, del_set,act_step):
            import re
            # input_string = "A(12,34,56,78,90)"
            # 使用正则表达式匹配括号内的内容
            match = re.search(r'\(([^)]+)\)', parent_name)
            first_value=-1
            if match:
                # 提取第一个逗号分隔的部分
                content = match.group(1)
                first_value = content.split(',')[0]
            return self.generate_action_name(index,first_value,pre,add, del_set,act_step)
            # pre_str = frozenset_to_str(pre)
            # add_str = frozenset_to_str(add)
            # del_set_str = frozenset_to_str(del_set)
            # return f"A({first_value}_{index},{pre_str},{add_str},{del_set_str},{act_step})"

        split_actions = []
        num_splits = random.randint(min_splits, max_splits)

        current_pre = action.pre

        # Ensure the last split gets whatever remains
        for i in range(num_splits):

            if i==num_splits-1:
                new_add = action.add
            else:
                new_add = frozenset({f"C({self.unique})"})
                self.unique += 1

            new_pre = current_pre
            current_pre = new_add

            act_step = random.randint(1,self.max_action_steps)
            new_name = generate_split_action_name(action.name, i,frozenset(new_pre), frozenset(new_add), frozenset(),act_step)

            # new_action = PlanningAction(new_name, current_pre, new_add, new_del,cost=0)
            new_action = PlanningAction(new_name, frozenset(new_pre), frozenset(new_add), frozenset())

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

data_generator = DataGenerator()
datasets = [data_generator.generate_dataset() for _ in range(num_data)]

for i, dataset in enumerate(datasets):
    data_generator.save_tree_as_dot(dataset, f'{i}_generated_tree.dot')
