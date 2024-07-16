# Generated from BTMLParser.g4 by ANTLR 4.13.1
from antlr4 import *

from mabtpg.behavior_tree.btml.grammar.BTMLParser import BTMLParser
from mabtpg.behavior_tree.btml.grammar.BTMLParserListener import BTMLParserListener
import shortuuid
# import py_trees as ptree
# from mabtpg.behavior_tree.base_nodes import Inverter,Selector,Sequence
# from mabtpg.behavior_tree.base_nodes.AbsAct import AbsAct
# from mabtpg.behavior_tree.base_nodes.AbsCond import AbsCond
from mabtpg.utils.any_tree_node import AnyTreeNode

from .BTML import BTML


short_uuid = lambda: shortuuid.ShortUUID().random(length=8)


class BTMLListener(BTMLParserListener):
    """Translate the btml language to BT.

    Args:
        btmlListener (_type_): _description_
    """

    def __init__(self, scene=None, behaviour_lib_path=None) -> None:
        super().__init__()
        self.btml = BTML()
        self.stack = []

        self.scene = scene
        self.behaviour_lib_path = behaviour_lib_path

    # Enter a parse tree produced by BTMLParser#root.
    def enterRoot(self, ctx: BTMLParser.RootContext):
        self.current_tree = self.btml
        self.stack = []


    # Exit a parse tree produced by BTMLParser#root.
    def exitRoot(self, ctx: BTMLParser.RootContext):
        pass


    # Enter a parse tree produced by BTMLParser#behavior_def.
    def enterBehavior_def(self, ctx:BTMLParser.Behavior_defContext):
        def_btml = BTML()
        node_type = str(ctx.children[1])
        literal = ctx.literal()
        cls_name = str(literal.String())

        # if have params
        args = []
        if literal.behavior_parm():
            params = literal.behavior_parm()
            for i in params.children:
                if str(i) != ',':
                    args.append(f"{i}")

        # node = AnyTreeNode(node_type, cls_name, args)
        # node = AnyTreeNode('composite_action', cls_name, args)
        def_btml.cls_name = cls_name
        def_btml.var_args = args
        self.btml.sub_btml_dict[cls_name] = def_btml
        self.current_tree = def_btml
        self.stack = []

    # Exit a parse tree produced by BTMLParser#behavior_def.
    def exitBehavior_def(self, ctx:BTMLParser.Behavior_defContext):
        pass


    # Enter a parse tree produced by BTMLParser#tree.
    def enterTree(self, ctx: BTMLParser.TreeContext):
        node_type = str(ctx.internal_node().children[0])
        node = AnyTreeNode(node_type)

        self.stack.append(node)

    # Exit a parse tree produced by BTMLParser#tree.
    def exitTree(self, ctx: BTMLParser.TreeContext):
        if len(self.stack) >= 2:
            child = self.stack.pop()
            self.stack[-1].add_child(child)
        else:
            self.current_tree.anytree_root = self.stack[0]


    # Enter a parse tree produced by BTMLParser#Behavior_sign.
    def enterBehavior_sign(self, ctx: BTMLParser.Behavior_signContext):
        # Condition / Action
        node_type = str(ctx.children[0])
        literal_list = ctx.literal()

        node_list = []
        for literal in literal_list:
            cls_name = str(literal.String())

            # if have params
            args = []
            # if str(ctx.children[0]) != 'not' and len(ctx.children) > 4:
            if literal.behavior_parm():
                params = literal.behavior_parm()
                for i in params.children:
                    if str(i) != ',':
                        args.append(f"{i}")

            node = AnyTreeNode(node_type, cls_name, args)
            node_list.append(node)

        if len(literal_list) > 1:

            sequence_node = AnyTreeNode('sequence')
            sequence_node.add_children(node_list)

            sub_btml = BTML()
            sub_btml.anytree_root = sequence_node

            self.stack[-1].add_child(AnyTreeNode("composite_condition",cls_name=None, info={"sub_btml":sub_btml}))
        else:
            self.stack[-1].add_child(node_list[0])

        # if have 'not' decorator
        # if str(ctx.children[1]) == 'Not':
        #     upper_node = AnyTreeNode(node_type="Inverter", children=[node])
        #     # connect
        #     self.stack[-1].add_child(upper_node)
        # else:
            # connect



del BTMLParser