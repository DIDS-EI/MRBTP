import random
import networkx as nx
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.envs.computation_env.numerical_env.numsim_tools import frozenset_to_str
import numpy as np

random.seed(0)
np.random.seed(0)

class PlanningAction:
    def __init__(self, pre, add, del_set):
        self.pre = pre
        self.add = add
        self.del_set = del_set
        self.name = ""

class DatasetGenerator:
    def __init__(self, max_leaves, max_branch, max_depth, max_action_steps):
        self.max_leaves = max_leaves
        self.max_branch = max_branch
        self.max_depth = max_depth
        self.max_action_steps = max_action_steps
        self.unique = 1

    def generate_action_name(self, level, action_index, pre, add, del_set, act_step):
        # Dummy function to generate action names
        return f"Action{action_index}"

    def generate_dataset(self):
        random.seed(0)
        np.random.seed(0)

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
                    num_children = random.randint(1, min(self.max_branch, self.max_leaves))
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
        nx.drawing.nx_pydot.write_dot(G, "network_graph.dot")

        return G

    def propagate_states(self, graph):
        node_states = {n: frozenset() for n in graph.nodes}  # 初始化所有节点的状态为空集
        topo_sorted_nodes = list(nx.topological_sort(graph))  # 拓扑排序，确定遍历顺序

        for node in topo_sorted_nodes:
            current_state = node_states[node]
            for successor in graph.successors(node):
                new_elements = frozenset({f"C({self.unique})"})
                self.unique += 1
                action = PlanningAction(pre=current_state, add=new_elements, del_set=set())
                node_states[successor] = frozenset.union(node_states[successor], current_state, new_elements)

                # 更新边的属性，包括动作名称作为边的标签
                graph.edges[node, successor]['label'] = action.name
                graph.nodes[successor]['label'] = frozenset_to_str(node_states[successor])  # 更新节点的标签

        return node_states, graph

def frozenset_to_str(fs):
    return ', '.join(fs)

# 在主函数中调用这个函数，并保存图形
if __name__ == '__main__':
    generator = DatasetGenerator(max_leaves=3, max_branch=2, max_depth=3, max_action_steps=5)
    graph = generator.generate_dataset()
    node_states, updated_graph = generator.propagate_states(graph)
    nx.drawing.nx_pydot.write_dot(updated_graph, "updated_network_graph.dot")
