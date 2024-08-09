import random
import networkx as nx
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.envs.numerical_env.numsim_tools import frozenset_to_str,convert_cstr_set_to_num_set
from mabtpg.utils.tools import print_colored
import numpy as np

random.seed(0)
np.random.seed(0)


class DataGenerator:
    def __init__(self, max_depth=3, max_branch=5,cmp_ratio=0.5,max_cmp_act_split=5,max_action_steps=5,need_split_action=True, num_agent=2, max_num_data=100):

        self.max_depth=max_depth
        self.max_branch = max_branch
        self.cmp_ratio = cmp_ratio
        self.max_cmp_act_split = max_cmp_act_split
        self.max_action_steps = max_action_steps
        self.need_split_action = need_split_action

        self.num_agent = num_agent

        self.unique = 1

        self.datasets=[self.generate_data() for _ in range(max_num_data)]

    def generate_tree_struct(self):

        G = nx.DiGraph()  # 创建一个有向图

        action_index = 1
        node_index = 0  # 节点索引开始

        goal_state = frozenset({"C(0)"})
        G.add_node(node_index, label=str(goal_state), depth=0)

        frontier = [(goal_state, 0, node_index)]  # (状态, 深度, 节点索引)

        while frontier:
            new_frontier = []
            for state, depth, parent_index in frontier:
                if depth < self.max_depth:
                    num_children = random.randint(1, self.max_branch)
                    for _ in range(num_children):
                        new_state = frozenset()
                        action = PlanningAction(pre=state, add=new_state, del_set=set())
                        action.name = self.generate_action_name(depth + 1, action_index, state, new_state, set(), 1)
                        action_index += 1

                        node_index += 1
                        G.add_node(node_index, label=str(new_state), depth=depth + 1)
                        G.add_edge(node_index,parent_index, label=action.name)

                        new_frontier.append((new_state, depth + 1, node_index))

            frontier = new_frontier

        # 使用 pydot 保存为 DOT 文件
        # nx.drawing.nx_pydot.write_dot(G, "network_graph.dot")

        return G


    def propagate_states(self, graph):
        total_actions_ls = []

        node_states = {n: frozenset() for n in graph.nodes}  # 初始化所有节点的状态为空集
        topo_sorted_nodes = list(nx.topological_sort(graph))  # 拓扑排序，确定遍历顺序

        for node in topo_sorted_nodes:
            current_state = node_states[node]
            for successor in graph.successors(node):
                new_elements = frozenset({f"C({self.unique})"})

                action = PlanningAction(pre=current_state, add={f"C({self.unique})"}, del_set=set())
                act_step = random.randint(1,self.max_action_steps)
                action.name = self.generate_action_name(0, self.unique, action.pre, action.add, action.del_set, act_step)
                total_actions_ls.append(action)
                self.unique += 1

                node_states[successor] = frozenset.union(node_states[successor], current_state, new_elements)

                # 更新边的属性，包括动作名称作为边的标签
                graph.edges[node, successor]['label'] = action.name
                graph.nodes[successor]['label'] = frozenset_to_str(node_states[successor])  # 更新节点的标签

        goal = node_states[topo_sorted_nodes[-1]]
        return node_states, graph, goal, total_actions_ls


    def generate_data(self,seed=0):



        self.unique=1
        graph = self.generate_tree_struct()
        node_states, updated_graph,goal,total_actions_ls = self.propagate_states(graph)
        # nx.drawing.nx_pydot.write_dot(updated_graph, "updated_network_graph.dot")


        goal = frozenset(goal)
        start = frozenset()

        dataset = {
            'goal': goal,
            'goal_num': convert_cstr_set_to_num_set(goal),
            'start': start,
            'start_num': convert_cstr_set_to_num_set(start),
            'nodes': {n: graph.nodes[n]['label'] for n in graph.nodes()},  # 提取节点标签作为状态
            'edges': [(u, v, d['label']) for u, v, d in graph.edges(data=True)], # 提取边和动作名

            "CABTP_expanded_num": 0,


            'comp_btml_ls': {},
            'actions_cmp': [],# 原来的动作，组合动作只是名字变了

            'total_actions': [], #所有动作包括组合动作，包括split后的动作
            "action_num": 0,

            "split_actions_dict":{},
            "agent_actions_with_cmp":[],
            "agent_actions_without_cmp":[]
        }

        # cut composition to sub actions
        if self.need_split_action:
            (dataset['actions_cmp'], dataset['total_actions'],
             dataset['comp_btml_ls'], dataset['CABTP_expanded_num'],\
                dataset["split_actions_dict"] ) = \
                self.split_actions_and_plan_sub_btml(total_actions_ls)

            dataset["action_num"]= len(dataset['total_actions'])

        self.assign_actions_to_agents(dataset,num_agent=self.num_agent)

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
        new_actions_cmp = [] # 和原来动作数一样，只是改变组合动作的名字
        new_total_actions = []
        for act_id,action in enumerate(actions):
            if random.random() < self.cmp_ratio:
                split_action_ls = self.split_action_to_sub_actions(action, min_splits=2, max_splits=self.max_cmp_act_split)
                print_colored(f"Act Split :{action.name} pre:{action.pre} add:{action.add} del:{action.del_set}", color='blue')

                action.name = generate_composition_action_name(action.name)
                action.cost = 0
                split_actions_dict[action] = split_action_ls

                new_total_actions.extend(split_action_ls)

            new_actions_cmp.append(action)
            new_total_actions.append(action)

                # without_cmp
                # new_actions_without_cmp.remove(action)
                # new_actions_without_cmp.extend(split_action_ls)

                # with_cmp
                # new_actions_with_cmp.extend(split_action_ls)
                # action.name = generate_composition_action_name(action.name)
                # action.cost = 0
                # split_actions_dict[action] = split_action_ls

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
        return new_actions_cmp, new_total_actions, comp_actions_BTML_dic,CABTP_expanded_num,split_actions_dict


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

    def assign_actions_to_agents(self, dataset, num_agent=None):
        """
        Assign actions to agents.

        Args:
        - dataset: The dataset containing actions.
        - num_agent: The number of agents.

        Returns:
        - agent_actions: A list of lists, where each sublist contains actions assigned to an agent.
        - dataset["agent_actions_with_cmp"]
        - dataset["agent_actions_without_cmp"]
        """
        def assign_an_act_to_agent_ls(assigned_agents,action):
            if action in dataset["split_actions_dict"]:
                for agent_index in assigned_agents:
                    # print("agent_index:",agent_index)
                    agents_actions[agent_index].append(action)
                    agents_without_cmp[agent_index].extend(dataset["split_actions_dict"][action])
            else:
                for agent_index in assigned_agents:
                    agents_actions[agent_index].append(action)
                    agents_without_cmp[agent_index].append(action)


        if num_agent != None:
            self.num_agent = num_agent

        # if with_comp_action==True:
        #     datasets_actions = dataset["actions_with_cmp"]
        # else:
        #     datasets_actions = dataset["actions_without_cmp"]

        # Allocate actions to each agent
        agents_actions = [[] for _ in range(self.num_agent)]
        agents_without_cmp = [[] for _ in range(self.num_agent)]

        for action in dataset["actions_cmp"]:
            # Randomly choose at least one agent
            num_assignments = random.randint(1, num_agent)
            assigned_agents = random.sample(range(num_agent), num_assignments)

            # if is composition action
            assign_an_act_to_agent_ls(assigned_agents,action)

        # Check if each agent has at least one action; if not, randomly assign one
        for i in range(num_agent):
            if not agents_actions[i]:  # If the agent has no actions assigned
                # Randomly choose an action to assign to this agent
                action_to_assign = random.choice(dataset["actions_cmp"])
                assign_an_act_to_agent_ls([i],action_to_assign)

        # Print the allocation result to see the action list of each agent
        for i, actions in enumerate(agents_actions):
            print(f"Agent {i + 1} actions:")
            for action in actions:
                print(f"  act:{action.name} pre:{action.pre} add:{action.add} del:{action.del_set}")

        dataset["agent_actions_with_cmp"] = agents_actions
        dataset["agent_actions_without_cmp"] = agents_without_cmp

        # return agents_actions,agents_without_cmp

    def save_tree_as_dot(self, dataset, filename):
        G = nx.DiGraph()
        nodes = dataset['nodes']
        edges = dataset['edges']

        for node, state in nodes.items():
            G.add_node(node, label=str(state))

        for parent, child, action_name in edges:
            G.add_edge(child, parent, label=action_name)

        nx.drawing.nx_pydot.write_dot(G, filename)


# Usage example
# num_data = 1
# num_elements = 10
# max_depth = 3
#
# data_generator = DataGenerator()
# datasets = [data_generator.generate_data() for _ in range(num_data)]
#
# for i, dataset in enumerate(datasets):
#     data_generator.save_tree_as_dot(dataset, f'{i}_generated_tree.dot')
