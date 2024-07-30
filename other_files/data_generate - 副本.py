import random
import string
import networkx as nx
from mabtpg.utils.tools import print_colored
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
# from numsim_tools import Action

import numpy as np
random.seed(0)
np.random.seed(0)

class DataGenerator:
    def __init__(self, num_elements=10, total_elements_set=None, max_depth=2):
        self.num_elements = num_elements
        if total_elements_set==None:
            self.total_elements_set = frozenset(range(num_elements))
        else:
            self.total_elements_set = frozenset(total_elements_set)
        self.max_depth = max_depth

    def get_parts_from_state(self, state):
        part_num = random.randint(1, min(3, len(state)))
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
        print_colored(f"State Split {state} into {parts}", color='orange')
        return parts

    def generate_random_state(self):
        num = random.randint(min(self.num_elements,5), self.num_elements)
        return frozenset(random.sample(self.total_elements_set, num))

    def generate_random_goal(self):
        num_goal = random.randint(min(self.num_elements,5), int(self.num_elements / 2))
        return frozenset(random.sample(self.total_elements_set, num_goal))


    def generate_dataset(self):
        goal = self.generate_random_goal()
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

                parts = self.get_parts_from_state(leaf)
                for part in parts:
                    new_state, action = self.generate_start_and_action(part, leaf)
                    action.name = self.generate_action_name(depth, action_index)
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
            'start': start,
            'actions': actions,
            'nodes': nodes,
            'edges': edges
        }
        return dataset

    def generate_start_and_action(self, goal, leaf):
        action = PlanningAction()
        action.generate_from_goal(goal, self.num_elements, self.total_elements_set)

        # Ensure action.del_set does not contain any element from leaf
        action.del_set -= leaf

        # Ensure action.add is not empty
        if not action.add:
            element_to_add = random.choice(list(goal))
            action.add.add(element_to_add)

        # Calculate start state
        start = (goal - action.add) | action.del_set

        # Ensure start is not empty
        if not start:
            # If start is empty, add any arbitrary element, here we use 0 for simplicity
            # element_to_add = random.randint(0,  num_elements)  # Choosing a number outside the goal range for uniqueness
            element_to_add = random.choice(list(self.total_elements_set))
            start.add(element_to_add)
            action.pre.add(element_to_add)

        # Ensure action.pre is a subset of start
        if not action.pre <= start:
            start |= action.pre
            # action.pre = start & action.pre

            # additional_pre = start - action.pre
            # action.pre.update(additional_pre)

        action.pre = frozenset(action.pre-action.add)
        action.add = frozenset(action.add)
        action.del_set = frozenset(action.del_set-goal)

        return frozenset(start), action


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


    def generate_action_name(self,depth, index):
        alphabet = string.ascii_uppercase
        # first_letter = alphabet[index % 26]
        # second_letter = depth
        return f"A{index}({depth})"

    def split_action(self,action, min_splits=2, max_splits=4):
        def generate_split_action_name(parent_name, index):
            return f"SUB{parent_name}_{index}"

        add_elements = list(action.add)
        num_splits = random.randint(min_splits, min(len(add_elements), max_splits))
        random.shuffle(add_elements)

        split_actions = []
        current_pre = action.pre
        remaining_add = set(action.add)
        remaining_del = set(action.del_set)

        # Ensure the last split gets whatever remains
        for i in range(num_splits):
            new_name = generate_split_action_name(action.name, i)
            if i == num_splits - 1:
                new_add = remaining_add
                new_del = remaining_del
            else:
                num_add_to_take = max(1, len(remaining_add) // (num_splits - i))
                new_add = set(random.sample(list(remaining_add), num_add_to_take))
                remaining_add -= new_add

                num_del_to_take = max(1, len(remaining_del) // (num_splits - i))
                if len(remaining_del)==0:
                    new_del = set()
                else:
                    new_del = set(random.sample(list(remaining_del), num_del_to_take))
                remaining_del -= new_del

            new_action = PlanningAction(new_name, current_pre, new_add, new_del)
            current_pre = new_add

            split_actions.append(new_action)

        return split_actions


# Usage example
num_data = 1
num_elements = 10
max_depth = 3

data_generator = DataGenerator(num_elements=num_elements,  max_depth=max_depth)
datasets = [data_generator.generate_dataset() for _ in range(num_data)]

for i,dataset in enumerate(datasets):
    data_generator.save_tree_as_dot(dataset, f'{i}_generated_tree.dot')
