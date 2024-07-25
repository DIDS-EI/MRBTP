import random
import string
import networkx as nx
from numsim_tools import *
from mabtpg.utils.tools import print_colored

def get_parts_from_state(state):
    part_num = random.randint(1, min(3,len(state)))
    state_list = list(state)
    random.shuffle(state_list)

    # Create the partitions
    parts = [set() for _ in range(part_num)]

    # Distribute the elements of the state randomly to ensure each part is non-empty
    for i, element in enumerate(state_list):
        parts[i % part_num].add(element)

    # Ensure that each part is non-empty
    non_empty_parts = [part for part in parts if part]
    empty_parts_count = part_num - len(non_empty_parts)

    # Redistribute elements to empty parts if any
    if empty_parts_count > 0:
        for _ in range(empty_parts_count):
            random_part = random.choice(non_empty_parts)
            element_to_move = random_part.pop()
            empty_part = next(part for part in parts if not part)
            empty_part.add(element_to_move)
            if random_part:  # If the original part is still non-empty
                non_empty_parts.append(random_part)
    print_colored(f"State Split {state} into {parts}", color='orange')
    return parts



def generate_dataset(num_elements, total_elements_set,max_depth):

    goal = generate_random_goal(num_elements, total_elements_set)
    start = set()
    actions = []
    leaves = [(goal, 0)]  # (state, depth)
    node_index = 0
    nodes = {node_index: goal}
    edges = []
    node_index += 1
    action_index = 0

    while leaves:
        current_leaves = []
        for leaf, depth in leaves:
            if depth >= max_depth:
                continue

            parts = get_parts_from_state(leaf)
            for part in parts:
                new_state,action = generate_start_and_action(part,leaf,num_elements,total_elements_set)
                action.name = generate_action_name(depth, action_index)
                action_index += 1

                action.add_part = (part)

                actions.append(action)
                current_leaves.append((new_state, depth + 1))
                nodes[node_index] = new_state
                edges.append((list(nodes.keys())[list(nodes.values()).index(leaf)], node_index, action.name+"_"+str(action.add_part)))
                node_index += 1

        # 如果当前深度的叶子节点被处理完了，将这些叶子节点合并到 start 中
        if not current_leaves:
            for leaf, _ in leaves:
                start |= leaf
        leaves = current_leaves

    for leaf, _ in leaves:
        start |= leaf

    start = frozenset(start)
    dataset = {
        'goal': goal,
        'start': start,
        'actions': actions,
        'nodes': nodes,
        'edges': edges
    }
    return dataset


def save_tree_as_dot(dataset, filename):
    G = nx.DiGraph()
    nodes = dataset['nodes']
    edges = dataset['edges']

    for node, state in nodes.items():
        G.add_node(node, label=str(state))

    for edge in edges:
        parent, child, action_name = edge
        G.add_edge( child, parent, label=action_name)

    nx.drawing.nx_pydot.write_dot(G, filename)

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



# generate data
num_data = 1
num_elements = 10
num_cond_pred=5
num_obj=2

# 生成谓词列表
predicates = generate_predicates(num_cond_pred)

# 随机生成每个谓词对应的物体数目，并确保总数目为 num_elements
total_elements_set = set()
while len(total_elements_set) < num_elements:
    predicate = random.choice(predicates)
    obj = random.randint(1, num_obj)
    element = f"{predicate}({obj})"
    total_elements_set.add(element)
# 确保总数目为 num_elements
while len(total_elements_set) > num_elements:
    total_elements_set.pop()

total_elements_set = frozenset(total_elements_set)
print("Generated total_elements_set:", total_elements_set)

datasets = []
for _ in range(num_data):
    dataset = generate_dataset(num_elements=num_elements, total_elements_set=total_elements_set, max_depth=1)
    datasets.append(dataset)

# print and save as .dot
for dataset in datasets:
    # print_dataset(dataset)
    print_action_data_table(dataset['goal'], dataset['start'], dataset['actions'])
    save_tree_as_dot(dataset, 'generated_tree.dot')




#############################################################################################
print_colored("======================================================================================", "blue")
dataset = datasets[0]
num_agent = 2
# 分配动作给智能体

# 用现在的数据，生成更多的action
# 对于每个动作，如果 add>=3, 把它分割成2-4个动作
new_actions = list(dataset['actions'])

# SUB ACTION
# for action in dataset['actions']:
#     # print_colored(f"act:{action.name} pre:{action.pre} add:{action.add} del:{action.del_set}",color='blue')
#     if len(action.add)>=3:
#     # if random.random() < 0.5:
#         split_action_ls = split_action(action,min_splits=2,max_splits=5)
#         print_colored(f"Act Split :{action.name} pre:{action.pre} add:{action.add} del:{action.del_set}", color='blue')
#         # print_action_data_table(set(), set(), split_action_ls)
#         new_actions.extend(split_action_ls)

# 分配动作给智能体
agent_actions = [[] for _ in range(num_agent)]
for action in new_actions:
    # 随机选择至少一个智能体
    num_assignments = random.randint(1, num_agent)
    assigned_agents = random.sample(range(num_agent), num_assignments)
    for agent_index in assigned_agents:
        agent_actions[agent_index].append(action)

dataset['agent_actions'] = agent_actions
dataset['num_agent'] = num_agent

# 输出结果

for i, actions in enumerate(dataset['agent_actions']):
    print(f"Agent {i + 1} actions:")
    for action in actions:
        print(f"  act:{action.name} pre:{action.pre} add:{action.add} del:{action.del_set}")

# 跑一下算法看看效果

from DMR import DMR
dmr = DMR(dataset["goal"], dataset["start"], dataset["agent_actions"], dataset["num_agent"])
dmr.planning()

# 要tick进行测试，能否从 start 到 goal。
# 要几步
done = False
# while not done:

print_colored("======================================================================================", "blue")
for i in range(num_agent):
    print_colored(f"---AGENT - {i}---", color="yellow")
    # print(dmr.default_bt_ls[i])
    # dmr.default_bt_ls[i].tick(dataset["start"])



robot_list = dmr.default_bt_ls
state = dataset["start"]

steps = 0
canrun,have_success,have_running,all_fail = False,False,False,True
running_actions=[]
for rob in robot_list:
    val, obj = rob.tick(state)
    if val == 'success' or val == 'running':
        canrun = True
        all_fail = False
    if val == 'success':
        have_success = True
    if val == 'running':
        have_running = True
        running_actions.append(obj)






print(f"\ntask finished!")