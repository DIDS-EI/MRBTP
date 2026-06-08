import os
import importlib.util
from mabtpg.utils.path import get_root_path

# NOTE: the legacy ``load_btml`` / ``load_bt_from_btml`` functions used to live
# here and depended on ``mabtpg.behavior_tree.btml.bak.btmlCompiler``, which was
# removed in commit 91bb4f9 (refactor of the ANTLR-generated parser).
# The replacement API is exposed at the package level:
#
#     from mabtpg.behavior_tree.btml import load_btml
#     btml = load_btml("path/to/tree.btml")
#
# No code in ``mabtpg`` / ``test_experiment`` / ``test_multi_minigrid_single_demo``
# imports the old functions, so they are simply removed.


def print_tree_from_root(node, indent=0):
    """
    Recursively prints the tree, each child with increased indentation.

    :param node: The current tree node to print.
    :param indent: The number of '\t' to prefix the line with.
    """
    # 打印当前节点，增加缩进来表示层级
    print(f"{'    ' * indent}{node.print_name}")
    # 如果该节点有子节点，递归打印子节点
    if hasattr(node, "children"):
        for child in node.children:
            print_tree_from_root(child, indent + 1)

def find_node_by_name(tree, name):
    """
    Find a node in the behavior tree with the specified name.

    :param tree: The root of the behavior tree or subtree.
    :param name: The name of the node to find.
    :return: Node with the specified name, or None if not found.
    """
    if tree.name == name:
        return tree
    elif hasattr(tree, "children"):  # Check if the tree has children
        for child in tree.children:
            result = find_node_by_name(child, name)
            if result is not None:
                return result
    return None



def get_classes_from_folder(folder_path):
    cls_dict = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.py'):
            # 构建模块的完整路径
            module_path = os.path.join(folder_path, filename)
            # 获取模块名（不含.py扩展名）
            module_name = os.path.splitext(filename)[0]

            # 动态导入模块
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # 获取模块中定义的所有类
            for name, obj in module.__dict__.items():
                if isinstance(obj, type):
                    cls_dict[module_name] = obj

    return cls_dict


def load_behavior_tree_lib():
    root_path = get_root_path()
    type_list = ["Action","Condition"]
    behavior_dict = {}
    for type in type_list:
        path = os.path.join(root_path,"mabtpg.behavior_tree","behavior_lib",type)
        behavior_dict[type] = get_classes_from_folder(path)

    return behavior_dict

if __name__ == '__main__':
    print(load_behavior_tree_lib())
# class BehaviorTree(ptree):
#     def __init__(self):
#         super().__init__()