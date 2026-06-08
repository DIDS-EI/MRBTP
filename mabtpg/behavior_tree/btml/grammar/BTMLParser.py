# Generated from BTMLParser.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

if "." in __name__:
    from .BTMLParserBase import BTMLParserBase
else:
    from BTMLParserBase import BTMLParserBase

def serializedATN():
    return [
        4,1,20,74,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,1,0,1,0,1,0,5,0,18,8,0,10,0,12,0,21,9,0,1,0,1,0,1,1,1,1,1,1,1,
        1,5,1,29,8,1,10,1,12,1,32,9,1,1,1,1,1,1,2,1,2,1,2,1,3,1,3,1,3,1,
        3,5,3,43,8,3,10,3,12,3,46,9,3,1,3,1,3,1,4,1,4,1,4,3,4,53,8,4,1,4,
        1,4,1,5,1,5,1,5,5,5,60,8,5,10,5,12,5,63,9,5,1,6,1,6,1,6,1,6,1,6,
        1,6,1,6,1,6,1,6,1,6,0,0,7,0,2,4,6,8,10,12,0,2,1,0,11,13,1,0,14,15,
        73,0,14,1,0,0,0,2,24,1,0,0,0,4,35,1,0,0,0,6,38,1,0,0,0,8,49,1,0,
        0,0,10,56,1,0,0,0,12,64,1,0,0,0,14,19,3,2,1,0,15,18,5,3,0,0,16,18,
        3,12,6,0,17,15,1,0,0,0,17,16,1,0,0,0,18,21,1,0,0,0,19,17,1,0,0,0,
        19,20,1,0,0,0,20,22,1,0,0,0,21,19,1,0,0,0,22,23,5,0,0,1,23,1,1,0,
        0,0,24,25,3,4,2,0,25,30,5,1,0,0,26,29,3,6,3,0,27,29,3,2,1,0,28,26,
        1,0,0,0,28,27,1,0,0,0,29,32,1,0,0,0,30,28,1,0,0,0,30,31,1,0,0,0,
        31,33,1,0,0,0,32,30,1,0,0,0,33,34,5,2,0,0,34,3,1,0,0,0,35,36,7,0,
        0,0,36,37,5,3,0,0,37,5,1,0,0,0,38,39,7,1,0,0,39,44,3,8,4,0,40,41,
        5,20,0,0,41,43,3,8,4,0,42,40,1,0,0,0,43,46,1,0,0,0,44,42,1,0,0,0,
        44,45,1,0,0,0,45,47,1,0,0,0,46,44,1,0,0,0,47,48,5,3,0,0,48,7,1,0,
        0,0,49,50,5,17,0,0,50,52,5,4,0,0,51,53,3,10,5,0,52,51,1,0,0,0,52,
        53,1,0,0,0,53,54,1,0,0,0,54,55,5,5,0,0,55,9,1,0,0,0,56,61,5,17,0,
        0,57,58,5,6,0,0,58,60,5,17,0,0,59,57,1,0,0,0,60,63,1,0,0,0,61,59,
        1,0,0,0,61,62,1,0,0,0,62,11,1,0,0,0,63,61,1,0,0,0,64,65,5,19,0,0,
        65,66,7,1,0,0,66,67,3,8,4,0,67,68,5,18,0,0,68,69,5,3,0,0,69,70,5,
        1,0,0,70,71,3,2,1,0,71,72,5,2,0,0,72,13,1,0,0,0,7,17,19,28,30,44,
        52,61
    ]

class BTMLParser ( BTMLParserBase ):

    grammarFileName = "BTMLParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'('", "')'", "','", "'{'", "'}'", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'parallel'", "<INVALID>", 
                     "<INVALID>", "'Not'", "<INVALID>", "':'" ]

    symbolicNames = [ "<INVALID>", "INDENT", "DEDENT", "NEWLINE", "OPEN_PAREN", 
                      "CLOSE_PAREN", "COMMA", "OPEN_BRACE", "CLOSE_BRACE", 
                      "LINE_COMMENT", "WS", "SEQUENCE", "SELECTOR", "PARALLEL", 
                      "ACT", "COND", "NOT", "String", "COLON", "DEF", "AND" ]

    RULE_root = 0
    RULE_tree = 1
    RULE_internal_node = 2
    RULE_behavior_sign = 3
    RULE_literal = 4
    RULE_behavior_parm = 5
    RULE_behavior_def = 6

    ruleNames =  [ "root", "tree", "internal_node", "behavior_sign", "literal", 
                   "behavior_parm", "behavior_def" ]

    EOF = Token.EOF
    INDENT=1
    DEDENT=2
    NEWLINE=3
    OPEN_PAREN=4
    CLOSE_PAREN=5
    COMMA=6
    OPEN_BRACE=7
    CLOSE_BRACE=8
    LINE_COMMENT=9
    WS=10
    SEQUENCE=11
    SELECTOR=12
    PARALLEL=13
    ACT=14
    COND=15
    NOT=16
    String=17
    COLON=18
    DEF=19
    AND=20

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class RootContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def tree(self):
            return self.getTypedRuleContext(BTMLParser.TreeContext,0)


        def EOF(self):
            return self.getToken(BTMLParser.EOF, 0)

        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(BTMLParser.NEWLINE)
            else:
                return self.getToken(BTMLParser.NEWLINE, i)

        def behavior_def(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BTMLParser.Behavior_defContext)
            else:
                return self.getTypedRuleContext(BTMLParser.Behavior_defContext,i)


        def getRuleIndex(self):
            return BTMLParser.RULE_root

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRoot" ):
                listener.enterRoot(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRoot" ):
                listener.exitRoot(self)




    def root(self):

        localctx = BTMLParser.RootContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_root)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 14
            self.tree()
            self.state = 19
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==3 or _la==19:
                self.state = 17
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [3]:
                    self.state = 15
                    self.match(BTMLParser.NEWLINE)
                    pass
                elif token in [19]:
                    self.state = 16
                    self.behavior_def()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 21
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 22
            self.match(BTMLParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TreeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def internal_node(self):
            return self.getTypedRuleContext(BTMLParser.Internal_nodeContext,0)


        def INDENT(self):
            return self.getToken(BTMLParser.INDENT, 0)

        def DEDENT(self):
            return self.getToken(BTMLParser.DEDENT, 0)

        def behavior_sign(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BTMLParser.Behavior_signContext)
            else:
                return self.getTypedRuleContext(BTMLParser.Behavior_signContext,i)


        def tree(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BTMLParser.TreeContext)
            else:
                return self.getTypedRuleContext(BTMLParser.TreeContext,i)


        def getRuleIndex(self):
            return BTMLParser.RULE_tree

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTree" ):
                listener.enterTree(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTree" ):
                listener.exitTree(self)




    def tree(self):

        localctx = BTMLParser.TreeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_tree)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 24
            self.internal_node()
            self.state = 25
            self.match(BTMLParser.INDENT)
            self.state = 30
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 63488) != 0):
                self.state = 28
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [14, 15]:
                    self.state = 26
                    self.behavior_sign()
                    pass
                elif token in [11, 12, 13]:
                    self.state = 27
                    self.tree()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 32
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 33
            self.match(BTMLParser.DEDENT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Internal_nodeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NEWLINE(self):
            return self.getToken(BTMLParser.NEWLINE, 0)

        def SEQUENCE(self):
            return self.getToken(BTMLParser.SEQUENCE, 0)

        def SELECTOR(self):
            return self.getToken(BTMLParser.SELECTOR, 0)

        def PARALLEL(self):
            return self.getToken(BTMLParser.PARALLEL, 0)

        def getRuleIndex(self):
            return BTMLParser.RULE_internal_node

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInternal_node" ):
                listener.enterInternal_node(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInternal_node" ):
                listener.exitInternal_node(self)




    def internal_node(self):

        localctx = BTMLParser.Internal_nodeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_internal_node)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 14336) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 36
            self.match(BTMLParser.NEWLINE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Behavior_signContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def literal(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BTMLParser.LiteralContext)
            else:
                return self.getTypedRuleContext(BTMLParser.LiteralContext,i)


        def NEWLINE(self):
            return self.getToken(BTMLParser.NEWLINE, 0)

        def ACT(self):
            return self.getToken(BTMLParser.ACT, 0)

        def COND(self):
            return self.getToken(BTMLParser.COND, 0)

        def AND(self, i:int=None):
            if i is None:
                return self.getTokens(BTMLParser.AND)
            else:
                return self.getToken(BTMLParser.AND, i)

        def getRuleIndex(self):
            return BTMLParser.RULE_behavior_sign

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBehavior_sign" ):
                listener.enterBehavior_sign(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBehavior_sign" ):
                listener.exitBehavior_sign(self)




    def behavior_sign(self):

        localctx = BTMLParser.Behavior_signContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_behavior_sign)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 38
            _la = self._input.LA(1)
            if not(_la==14 or _la==15):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 39
            self.literal()
            self.state = 44
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==20:
                self.state = 40
                self.match(BTMLParser.AND)
                self.state = 41
                self.literal()
                self.state = 46
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 47
            self.match(BTMLParser.NEWLINE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def String(self):
            return self.getToken(BTMLParser.String, 0)

        def OPEN_PAREN(self):
            return self.getToken(BTMLParser.OPEN_PAREN, 0)

        def CLOSE_PAREN(self):
            return self.getToken(BTMLParser.CLOSE_PAREN, 0)

        def behavior_parm(self):
            return self.getTypedRuleContext(BTMLParser.Behavior_parmContext,0)


        def getRuleIndex(self):
            return BTMLParser.RULE_literal

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteral" ):
                listener.enterLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteral" ):
                listener.exitLiteral(self)




    def literal(self):

        localctx = BTMLParser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_literal)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 49
            self.match(BTMLParser.String)
            self.state = 50
            self.match(BTMLParser.OPEN_PAREN)
            self.state = 52
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==17:
                self.state = 51
                self.behavior_parm()


            self.state = 54
            self.match(BTMLParser.CLOSE_PAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Behavior_parmContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def String(self, i:int=None):
            if i is None:
                return self.getTokens(BTMLParser.String)
            else:
                return self.getToken(BTMLParser.String, i)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(BTMLParser.COMMA)
            else:
                return self.getToken(BTMLParser.COMMA, i)

        def getRuleIndex(self):
            return BTMLParser.RULE_behavior_parm

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBehavior_parm" ):
                listener.enterBehavior_parm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBehavior_parm" ):
                listener.exitBehavior_parm(self)




    def behavior_parm(self):

        localctx = BTMLParser.Behavior_parmContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_behavior_parm)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 56
            self.match(BTMLParser.String)
            self.state = 61
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==6:
                self.state = 57
                self.match(BTMLParser.COMMA)
                self.state = 58
                self.match(BTMLParser.String)
                self.state = 63
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Behavior_defContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DEF(self):
            return self.getToken(BTMLParser.DEF, 0)

        def literal(self):
            return self.getTypedRuleContext(BTMLParser.LiteralContext,0)


        def COLON(self):
            return self.getToken(BTMLParser.COLON, 0)

        def NEWLINE(self):
            return self.getToken(BTMLParser.NEWLINE, 0)

        def INDENT(self):
            return self.getToken(BTMLParser.INDENT, 0)

        def tree(self):
            return self.getTypedRuleContext(BTMLParser.TreeContext,0)


        def DEDENT(self):
            return self.getToken(BTMLParser.DEDENT, 0)

        def ACT(self):
            return self.getToken(BTMLParser.ACT, 0)

        def COND(self):
            return self.getToken(BTMLParser.COND, 0)

        def getRuleIndex(self):
            return BTMLParser.RULE_behavior_def

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBehavior_def" ):
                listener.enterBehavior_def(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBehavior_def" ):
                listener.exitBehavior_def(self)




    def behavior_def(self):

        localctx = BTMLParser.Behavior_defContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_behavior_def)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 64
            self.match(BTMLParser.DEF)
            self.state = 65
            _la = self._input.LA(1)
            if not(_la==14 or _la==15):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 66
            self.literal()
            self.state = 67
            self.match(BTMLParser.COLON)
            self.state = 68
            self.match(BTMLParser.NEWLINE)
            self.state = 69
            self.match(BTMLParser.INDENT)
            self.state = 70
            self.tree()
            self.state = 71
            self.match(BTMLParser.DEDENT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





