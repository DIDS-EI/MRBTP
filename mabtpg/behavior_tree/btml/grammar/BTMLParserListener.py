# Generated from BTMLParser.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .BTMLParser import BTMLParser
else:
    from BTMLParser import BTMLParser

# This class defines a complete listener for a parse tree produced by BTMLParser.
class BTMLParserListener(ParseTreeListener):

    # Enter a parse tree produced by BTMLParser#root.
    def enterRoot(self, ctx:BTMLParser.RootContext):
        pass

    # Exit a parse tree produced by BTMLParser#root.
    def exitRoot(self, ctx:BTMLParser.RootContext):
        pass


    # Enter a parse tree produced by BTMLParser#tree.
    def enterTree(self, ctx:BTMLParser.TreeContext):
        pass

    # Exit a parse tree produced by BTMLParser#tree.
    def exitTree(self, ctx:BTMLParser.TreeContext):
        pass


    # Enter a parse tree produced by BTMLParser#internal_node.
    def enterInternal_node(self, ctx:BTMLParser.Internal_nodeContext):
        pass

    # Exit a parse tree produced by BTMLParser#internal_node.
    def exitInternal_node(self, ctx:BTMLParser.Internal_nodeContext):
        pass


    # Enter a parse tree produced by BTMLParser#behavior_sign.
    def enterBehavior_sign(self, ctx:BTMLParser.Behavior_signContext):
        pass

    # Exit a parse tree produced by BTMLParser#behavior_sign.
    def exitBehavior_sign(self, ctx:BTMLParser.Behavior_signContext):
        pass


    # Enter a parse tree produced by BTMLParser#literal.
    def enterLiteral(self, ctx:BTMLParser.LiteralContext):
        pass

    # Exit a parse tree produced by BTMLParser#literal.
    def exitLiteral(self, ctx:BTMLParser.LiteralContext):
        pass


    # Enter a parse tree produced by BTMLParser#behavior_parm.
    def enterBehavior_parm(self, ctx:BTMLParser.Behavior_parmContext):
        pass

    # Exit a parse tree produced by BTMLParser#behavior_parm.
    def exitBehavior_parm(self, ctx:BTMLParser.Behavior_parmContext):
        pass


    # Enter a parse tree produced by BTMLParser#behavior_def.
    def enterBehavior_def(self, ctx:BTMLParser.Behavior_defContext):
        pass

    # Exit a parse tree produced by BTMLParser#behavior_def.
    def exitBehavior_def(self, ctx:BTMLParser.Behavior_defContext):
        pass



del BTMLParser