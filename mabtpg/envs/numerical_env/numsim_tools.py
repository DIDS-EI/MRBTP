import random
import string
import numpy as np
import copy
import os
import re
import pickle
from tabulate import tabulate
random.seed(0)
np.random.seed(0)
import pandas as pd

class NumAction:
    def __init__(self, name, pre, add, del_set, act_step):
        """
        Initialize the Action object.

        Parameters:
        name (str): The name of the action.
        pre (frozenset): The preconditions of the action.
        add (frozenset): The add set of the action.
        del_set (frozenset): The delete set of the action.
        """
        self.name = name
        self.pre = pre
        self.add = add
        self.del_set = del_set
        self.act_step=act_step
        self.is_finish = False

    def to_dict(self):
        """
        Convert the Action object to a dictionary.

        Returns:
        dict: A dictionary representation of the Action object.
        """
        return {
            'name': self.name,
            'pre': self.pre,
            'add': self.add,
            'del_set': self.del_set,
        }



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


def create_directory_if_not_exists(dir_name):
    """
    Create a directory if it does not exist.

    Args:
    - dir_name: The name of the directory to create.
    """
    # Check if the directory exists
    if not os.path.exists(dir_name):
        # Create the directory
        os.makedirs(dir_name)
        print(f"Directory {dir_name} created.")
    else:
        print(f"Directory {dir_name} already exists.")


def load_data_from_directory(dir_name):
    """
    Load all data files from the specified directory using pickle.

    Args:
    - dir_name: The name of the directory to load data from.
    - num_elements: The number of elements in the data.
    - max_depth: The maximum depth of the data.

    Returns:
    - data_list: A list containing the loaded data.
    """
    data_list = []

    # Check if the directory exists
    if not os.path.exists(dir_name):
        print(f"Directory {dir_name} does not exist.")
        return data_list

    # List all files in the directory
    files = os.listdir(dir_name)
    files = [f for f in files if f.endswith('.pkl')]  # Assuming the data files are Pickle files

    # Load all data files
    for file_name in files:
        file_path = os.path.join(dir_name, file_name)
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
            data_list.append(data)

    return data_list

def convert_cstr_set_to_num_set(cstr_set):
    numbers = []
    for item in cstr_set:
        match = re.search(r'\d+', item)
        if match:
            numbers.append(int(match.group()))
    return frozenset(numbers)


def frozenset_to_str(fs):
    """
    Convert a frozenset of strings with embedded numbers to a comma-separated string of the numbers.

    Parameters:
    fs (frozenset): A frozenset of strings in the form 'C(number)'.

    Returns:
    str: A string containing the sorted numbers extracted from the frozenset, separated by commas.
    """
    numbers = convert_cstr_set_to_num_set(fs)
    return '_'.join(str(x) for x in sorted(numbers))

def str_to_frozenset(action_string):
    """
    Convert a string in the format "1_2_3_4" to a frozenset of integers.

    Parameters:
    action_string (str): The action string in the format "1_2_3_4".

    Returns:
    frozenset: A frozenset of integers extracted from the string.
    """
    elements = action_string.split('_')
    if elements==['']:
        return set()
    else:
        int_elements = [int(element) for element in elements]
    return frozenset(int_elements)


def get_action_name(action_name):

    if "A(" in action_name:
        import re
        # input_string = "A(12,34,56,78,90)"
        # 使用正则表达式匹配括号内的内容
        match = re.search(r'\(([^)]+)\)', action_name)
        first_value = -1
        if match:
            # 提取第一个逗号分隔的部分
            content = match.group(1)
            first_value = content.split(',')[0]
            action_name = first_value

    if "CMP" in action_name:
        return action_name

    # Convert a string in the format "{index}_{depth}" to "A{index}_D{depth}".
    parts = action_name.split('_')
    parent_name = ""
    if len(parts) == 2:
        index, depth = parts
        return f"A{index}_D{depth}"
    else:
        index,depth,sub = parts
        return f"A{index}_D{depth}_Sub{sub}"

def convert_to_num_frozenset(fs):
    """
    Convert a frozenset of strings with embedded numbers to a frozenset of integers.

    Parameters:
    fs (frozenset): A frozenset of strings in the form 'C(number)'.

    Returns:
    frozenset: A frozenset of integers extracted from the strings.
    """
    numbers = []
    for item in fs:
        match = re.search(r'\d+', item)
        if match:
            numbers.append(int(match.group()))
    return frozenset(numbers)


def save_tree_as_dot( dataset, filename):
    import networkx as nx
    G = nx.DiGraph()
    nodes = dataset['nodes']
    edges = dataset['edges']

    for node, state in nodes.items():
        G.add_node(node, label=str(state))

    for parent, child, action_name in edges:
        G.add_edge(child, parent, label=action_name)

    nx.drawing.nx_pydot.write_dot(G, filename)

def print_summary_table(summary_results, formatted=True):
    df = pd.DataFrame(summary_results)
    if formatted:
        print(df.to_string(index=False))
    else:
        print(df.to_csv(index=False, sep='\t'))