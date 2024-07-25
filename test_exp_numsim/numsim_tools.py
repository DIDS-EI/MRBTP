import random
import string
import numpy as np
import copy
from tabulate import tabulate
random.seed(1)
np.random.seed(1)

class Action:
    def __init__(self,name='anonymous action'):
        self.pre=set()
        self.add=set()
        self.del_set=set()
        self.name=name
        self.cost=1

        self.add_part = None

    def __str__(self):
        return self.name

    def generate_from_state(self,state,num):
        for i in range(0,num):
            if i in state:
                if random.random() >0.5:
                    self.pre.add(i)
                    if random.random() >0.5:
                        self.del_set.add(i)
                    continue
            if random.random() > 0.5:
                self.add.add(i)
                continue
            if random.random() >0.5:
                self.del_set.add(i)

    def print_action(self):
        print (self.pre)
        print(self.add)
        print(self.del_set)


    # from goal get act and start
    # def generate_from_goal(self, goal, num):
    #     added = False  # Flag to ensure at least one element is added
    #     for i in range(num):
    #         if i in goal:
    #             if random.random() > 0.5:
    #                 self.add.add(i)
    #                 added = True
    #                 if random.random() > 0.5:
    #                     self.pre.add(i)
    #         else:
    #             if random.random() > 0.5:
    #                 self.del_set.add(i)
    #                 if random.random() > 0.5:
    #                     self.pre.add(i)
    #
    #     # Ensure at least one element in add
    #     if not added:
    #         element_to_add = random.choice(list(goal))
    #         self.add.add(element_to_add)
    def generate_from_goal(self, goal, num, total_elements_set):
        added = False  # Flag to ensure at least one element is added
        for _ in range(num):
            element = random.choice(list(total_elements_set))
            if element in goal:
                if random.random() > 0.5:
                    self.add.add(element)
                    added = True
                    if random.random() > 0.5:
                        self.pre.add(element)
            else:
                if random.random() > 0.9:
                    self.del_set.add(element)
                    if random.random() > 0.5:
                        self.pre.add(element)

        # Ensure at least one element in add
        if not added:
            element_to_add = random.choice(list(goal))
            self.add.add(element_to_add)

def generate_start_and_action(goal, leaf, num_elements,total_elements_set):
    action = Action()
    action.generate_from_goal(goal, num_elements,total_elements_set)

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
        element_to_add = random.choice(list(total_elements_set))
        start.add(element_to_add)
        action.pre.add(element_to_add)

    # Ensure action.pre is a subset of start
    if not action.pre <= start:
        start |= action.pre
        # action.pre = start & action.pre

        # additional_pre = start - action.pre
        # action.pre.update(additional_pre)

    action.pre = frozenset(action.pre)
    action.add = frozenset(action.add)
    action.del_set = frozenset(action.del_set)

    return frozenset(start), action


def split_action(action, min_splits=2, max_splits=4):
    add_elements = list(action.add)
    num_splits = random.randint(min_splits, min(len(add_elements), max_splits))
    random.shuffle(add_elements)

    split_actions = []
    split_size = len(add_elements) // num_splits

    for i in range(num_splits):
        new_action = Action(name=f"{action.name}_split_{i+1}")
        new_action.name = generate_split_action_name(action.name,i)
        new_action.pre = action.pre if i == 0 else split_actions[-1].add
        new_action.del_set = action.del_set if i == num_splits - 1 else set()

        if i == num_splits - 1:
            new_action.add = set(add_elements[i * split_size:])
        else:
            new_action.add = set(add_elements[i * split_size:(i + 1) * split_size])

        split_actions.append(new_action)

    return split_actions


# def generate_random_state(num):
#     result = set()
#     for i in range(0,num):
#         if random.random()>0.5:
#             result.add(i)
#     return result

def generate_random_state(num_elements, total_elements_set):
    num = random.randint(min(num_elements,5), num_elements)
    return frozenset(random.sample(total_elements_set, num))

def generate_random_goal(num_elements, total_elements_set):
    num_goal = random.randint(min(num_elements,5), num_elements/2)
    return frozenset(random.sample(total_elements_set, num_goal))

def state_transition(state,action):
    if not action.pre <= state:
        print ('error: action not applicable')
        return state
    new_state=(state | action.add) - action.del_set
    return new_state

def ma_state_transition(state,action_list):
    new_state = state
    for action in action_list:
        if not action.pre <= state:
            print('error: action not applicable')
            print (action.name,action.pre,state)
            return state
    for action in action_list:
        new_state = (new_state | action.add) - action.del_set
    return new_state



def print_dataset(dataset):
    print("Goal:", dataset['goal'])
    print("Start:", dataset['start'])
    print("Actions:")
    for action in dataset['actions']:
        action.print_action()




def generate_action_name(depth, index):
    alphabet = string.ascii_uppercase
    # first_letter = alphabet[index % 26]
    # second_letter = depth
    return f"A{index}({depth})"

def generate_split_action_name(parent_name,index):
    alphabet = string.ascii_uppercase
    return f"SUB{parent_name}({index})"



def print_action_data_table(goal,start,actions):
    data = []
    for a in actions:
        data.append([a.name ,a.pre ,a.add ,a.del_set ,a.cost])
    data.append(["Goal" ,goal ," " ,"Start" ,start])
    print(tabulate(data, headers=["Name", "Pre", "Add" ,"Del" ,"Cost"], tablefmt="fancy_grid"))  # grid plain simple github fancy_grid
