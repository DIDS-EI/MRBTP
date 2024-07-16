from mabtpg.utils.any_tree_node import AnyTreeNode, traverse_and_modify_tree, new_tree_like

import copy


class BTML:
    def __init__(self):
        self.cls_name = None
        self.var_args = ()

        self.anytree_root = None
        self.sub_btml_dict = {}

    def clone_with_new_root(self,root):
        new_btml = BTML()
        new_btml.anytree_root = root
        new_btml.sub_btml_dict = copy.deepcopy(self.sub_btml_dict)
        return new_btml

    def instantiate(self, arg_dict):
        if not isinstance(arg_dict,dict):
            new_arg_dict = {}
            for i in range(len(self.var_args)):
                new_arg_dict[self.var_args[i]] = arg_dict[i]
            arg_dict = new_arg_dict

        def new_func(node):
            new_node = AnyTreeNode(node.node_type,node.cls_name)
            arg_list = []
            for i in range(len(node.args)):
                arg = node.args[i]
                if arg in arg_dict:
                    arg_list.append(arg_dict[arg])
                else:
                    arg_list.append(arg)

            new_node.args = arg_list
            if node.node_type == "composite_condition":
                new_btml = node.info['sub_btml'].instantiate(arg_dict)
                new_node.info = {'sub_btml':new_btml}

            return new_node

        new_tree = new_tree_like(self.anytree_root,new_func)
        # traverse_and_modify_tree(self.anytree_root, func)

        new_btml = BTML()
        new_btml.cls_name = self.cls_name
        new_btml.anytree_root = new_tree
        new_btml.sub_btml_dict = self.sub_btml_dict
        return new_btml