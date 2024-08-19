import random
import matplotlib.pyplot as plt
import networkx as nx

class Action:
    def __init__(self, name='anonymous action'):
        self.pre = set()
        self.add = set()
        self.del_set = set()
        self.name = name

    def __str__(self):
        return self.name

    def generate_from_state(self, state, num):
        for i in range(0, num):
            if i in state:
                if random.random() > 0.5:
                    self.pre.add(i)
                    if random.random() > 0.5:
                        self.del_set.add(i)
                    continue
            if random.random() > 0.5:
                self.add.add(i)
                continue
            if random.random() > 0.5:
                self.del_set.add(i)

    def print_action(self):
        print(self.pre)
        print(self.add)
        print(self.del_set)


def generate_random_state(num):
    result = set()
    for i in range(0, num):
        if random.random() > 0.5:
            result.add(i)
    return result


def state_transition(state, action):
    if not action.pre <= state:
        print('error: action not applicable')
        return state
    new_state = (state | action.add) - action.del_set
    return new_state


def ma_state_transition(state, action_list):
    new_state = state
    for action in action_list:
        if not action.pre <= state:
            print('error: action not applicable')
            print(action.name, action.pre, state)
            return state
    for action in action_list:
        new_state = (new_state | action.add) - action.del_set
    return new_state


def generate_dataset(data_num, num_elements, max_depth):
    datasets = []

    for _ in range(data_num):
        goal = generate_random_state(num_elements)
        g_part_num = random.randint(2, 5)
        goal_parts = [set() for _ in range(g_part_num)]

        goal_list = list(goal)
        random.shuffle(goal_list)
        for i, element in enumerate(goal_list):
            goal_parts[i % g_part_num].add(element)

        actions = []
        leaves = [(goal, 0)]  # (state, depth)
        node_index = 0
        nodes = {node_index: goal}
        edges = []
        node_index += 1

        while leaves:
            current_leaves = []
            for leaf, depth in leaves:
                if depth >= max_depth:
                    continue

                for part in goal_parts:
                    if random.random() < 0.8:  # 以0.8的概率继续分裂
                        action = Action(name=f'action_{depth}_{part}')
                        action.add = part.copy()
                        action.pre = part.copy()
                        if random.random() > 0.5:
                            action.del_set = set(random.sample(goal_list, random.randint(0, len(goal_list) // 2)))
                        action.del_set -= part
                        new_state = state_transition(leaf, action)
                        if new_state:
                            actions.append(action)
                            current_leaves.append((new_state, depth + 1))
                            nodes[node_index] = new_state
                            edges.append((list(nodes.keys())[list(nodes.values()).index(leaf)], node_index, action.name))
                            node_index += 1

            leaves = current_leaves

        start = set()
        for leaf, _ in leaves:
            start |= leaf

        dataset = {
            'goal': goal,
            'start': start,
            'actions': actions,
            'nodes': nodes,
            'edges': edges
        }

        datasets.append(dataset)

    return datasets


def print_dataset(dataset):
    print("Goal:", dataset['goal'])
    print("Start:", dataset['start'])
    print("Actions:")
    for action in dataset['actions']:
        action.print_action()


def draw_tree(dataset):
    G = nx.DiGraph()
    nodes = dataset['nodes']
    edges = dataset['edges']

    for node, state in nodes.items():
        G.add_node(node, label=str(state))

    for edge in edges:
        parent, child, action_name = edge
        G.add_edge(parent, child, label=action_name)

    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, 'label')
    edge_labels = nx.get_edge_attributes(G, 'label')

    nx.draw(G, pos, with_labels=True, labels=labels, node_size=3000, node_color="skyblue", font_size=10, font_weight="bold")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    plt.show()


# 生成数据集并绘制图形
datasets = generate_dataset(data_num=1, num_elements=10, max_depth=3)
for dataset in datasets:
    print_dataset(dataset)
    draw_tree(dataset)
