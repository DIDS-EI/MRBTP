# from mabtpg.behavior_tree.scene.scene import Scene
# from mabtpg.behavior_tree.behavior_tree.btml.btmlCompiler import load

import py_trees as ptree
from mabtpg.behavior_tree.utils.visitor import StatusVisitor
from mabtpg.utils.any_tree_node import traverse_and_modify_tree

from mabtpg.behavior_tree.utils.draw import render_dot_tree
from mabtpg.behavior_tree.utils.load import load_btml, print_tree_from_root

import os
from mabtpg.utils.path import get_root_path
from mabtpg.utils.any_tree_node import new_tree_like

from mabtpg.behavior_tree.base_nodes import base_node_map, composite_node_map,base_node_type_map

import sys

class BehaviorTree(ptree.trees.BehaviourTree):
    def __init__(self,anytree=None, behavior_lib=None):
        if isinstance(anytree,str):
            anytree = load_btml(anytree)

        self.behavior_lib = behavior_lib
        if behavior_lib:
            bt_root = new_tree_like(anytree,self.new_node_with_lib)
        else:
            bt_root = new_tree_like(anytree,self.new_node)

        super().__init__(bt_root)

        self.visitor = StatusVisitor()
        self.visitors.append(self.visitor)



    def new_node(self, node):
        if node.node_type in composite_node_map.keys():
            node_type = composite_node_map[node.node_type]
            return node_type(memory=False)
        else:
            node_type = base_node_map[node.node_type]
            cls_name = node.cls_name
            args = node.args
            return type(cls_name, (node_type,), {})(*args)

    def new_node_with_lib(self, node):
        if node.node_type in composite_node_map.keys():
            node_type = composite_node_map[node.node_type]
            return node_type(memory=False)
        else:
            node_type = base_node_type_map[node.node_type]
            cls_name = node.cls_name
            return self.behavior_lib[node_type][cls_name](*node.args)

    def bind_agent(self, agent):
        def func(node):
            node.agent = agent
            node.env = agent.env

        traverse_and_modify_tree(self.root,func)


    def print(self):
        print_tree_from_root(self.root)


    def save_btml(self,path):
        original_stdout = sys.stdout

        with open(path, 'w') as f:
            sys.stdout = f
            print_tree_from_root(self.root)

        sys.stdout = original_stdout

    def draw(self,file_name="behavior_tree",png_only=False):
        render_dot_tree(self.root,name=file_name,png_only=png_only)



if __name__ == '__main__':

    # create robot
    root_path = get_root_path()
    btml_path = os.path.join(root_path, 'mabtpg/behavior_tree/utils/draw_bt/Default.btml')
    behavior_lib_path = os.path.join(root_path, 'mabtpg/behavior_tree/exec_lib')
    bt = load_bt_from_btml(None, btml_path, behavior_lib_path)



    render_dot_tree(bt.root,name="llm_test",png_only = False)
    # build and tick
