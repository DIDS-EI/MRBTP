# from mabtpg.behavior_tree.scene.scene import Scene
# from mabtpg.behavior_tree.behavior_tree.btml.btmlCompiler import load

import py_trees as ptree
from mabtpg.behavior_tree.utils.visitor import StatusVisitor
from mabtpg.utils.any_tree_node import traverse_and_modify_tree

from mabtpg.behavior_tree.utils.draw import render_dot_tree
from mabtpg.behavior_tree.utils.load import print_tree_from_root
from mabtpg.behavior_tree.btml import load_btml

import os
from mabtpg.utils.path import get_root_path
from mabtpg.utils.any_tree_node import new_tree_like

from mabtpg.behavior_tree.base_nodes import base_node_map, control_node_map,base_node_type_map,composite_node_map

import copy
import sys

class BehaviorTree(ptree.trees.BehaviourTree):
    def __init__(self, btml=None, behavior_lib=None):
        if isinstance(btml, str):
            btml = load_btml(btml)

        self.btml = btml
        anytree_root = btml.bt_root
        self.behavior_lib = behavior_lib.clone()

        if behavior_lib:
            self.create_composite_behavior_lib()

        if behavior_lib:
            bt_root = new_tree_like(anytree_root, self.new_node_with_lib)
        else:
            bt_root = new_tree_like(anytree_root, self.new_node)

        super().__init__(bt_root)

        self.visitor = StatusVisitor()
        self.visitors.append(self.visitor)

    def create_composite_behavior_lib(self):
        for sub_btml in self.btml.composite_btml_list:
            node = sub_btml.anytree
            node_type = composite_node_map[node.node_type]
            cls_name = node.cls_name
            args = node.args

            composite_cls = type(cls_name, (node_type,), {})

            composite_cls.subtree_func = lambda _: BehaviorTree(sub_btml,self.behavior_lib)

            super_type = base_node_type_map[node.node_type]
            if cls_name in self.behavior_lib[super_type]:
                raise TypeError(f"{cls_name} already defined!")

            self.behavior_lib[super_type][cls_name] = composite_cls


    def clone(self):
        return copy.deepcopy(self)

    def new_node(self, node):
        if node.node_type in control_node_map.keys():
            node_type = control_node_map[node.node_type]
            return node_type(memory=False)
        elif node.node_type in base_node_type_map.keys():
            node_type = base_node_map[node.node_type]
            cls_name = node.cls_name
            args = node.args
            return type(cls_name, (node_type,), {})(*args)
        else:
            node_type = composite_node_map[node.node_type]
            args = node.args
            condition_list = []
            for anytree_condition in args:
                c_node_type = base_node_map[anytree_condition.node_type]
                cls_name = anytree_condition.cls_name
                c_args = anytree_condition.args
                condition_list.append(type(cls_name, (c_node_type,), {})(*c_args))
            return node_type(*condition_list)


    def new_node_with_lib(self, node):
        if node.node_type in control_node_map.keys():
            node_type = control_node_map[node.node_type]
            return node_type(memory=False)
        elif node.node_type in base_node_type_map.keys():
            node_type = base_node_type_map[node.node_type]
            cls_name = node.cls_name
            return self.behavior_lib[node_type][cls_name](*node.args)
        else:
            node_type = composite_node_map[node.node_type]
            cls_name = node.cls_name
            if cls_name:
            # def composite
                def_composite = self.btml.composite_behavior_lib[cls_name]
                subtree_root = def_composite.args
            else:
            # inline composite
                subtree_root = node.args

            subtree_btml = self.btml.clone_with_new_root(subtree_root.bt_root)
            sub_tree = BehaviorTree(subtree_btml,self.behavior_lib)

            return node_type(cls_name,sub_tree)


    def bind_agent(self, agent):
        def func(node):
            node.bind_agent(agent)

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
    btml_path = os.path.join(root_path, 'mabtpg/behavior_tree/utils/draw_bt/robot.bt')
    behavior_lib_path = os.path.join(root_path, 'mabtpg/behavior_tree/exec_lib')
    bt = load_bt_from_btml(None, btml_path, behavior_lib_path)



    render_dot_tree(bt.root,name="llm_test",png_only = False)
    # build and tick
