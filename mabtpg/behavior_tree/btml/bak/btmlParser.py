# Generated from btml_bracket.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,23,69,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,1,0,4,
        0,14,8,0,11,0,12,0,15,1,0,1,0,1,1,1,1,1,1,1,1,5,1,24,8,1,10,1,12,
        1,27,9,1,1,1,1,1,1,2,1,2,1,2,1,2,1,2,3,2,36,8,2,1,3,1,3,3,3,40,8,
        3,1,3,1,3,1,3,3,3,45,8,3,1,3,1,3,1,4,1,4,1,4,1,4,3,4,53,8,4,1,4,
        1,4,1,4,1,4,1,4,3,4,60,8,4,5,4,62,8,4,10,4,12,4,65,9,4,1,5,1,5,1,
        5,0,0,6,0,2,4,6,8,10,0,2,1,0,7,12,1,0,17,18,77,0,13,1,0,0,0,2,19,
        1,0,0,0,4,35,1,0,0,0,6,37,1,0,0,0,8,52,1,0,0,0,10,66,1,0,0,0,12,
        14,3,2,1,0,13,12,1,0,0,0,14,15,1,0,0,0,15,13,1,0,0,0,15,16,1,0,0,
        0,16,17,1,0,0,0,17,18,5,0,0,1,18,1,1,0,0,0,19,20,3,4,2,0,20,25,5,
        1,0,0,21,24,3,6,3,0,22,24,3,2,1,0,23,21,1,0,0,0,23,22,1,0,0,0,24,
        27,1,0,0,0,25,23,1,0,0,0,25,26,1,0,0,0,26,28,1,0,0,0,27,25,1,0,0,
        0,28,29,5,2,0,0,29,3,1,0,0,0,30,36,5,3,0,0,31,36,5,4,0,0,32,36,5,
        5,0,0,33,34,5,6,0,0,34,36,5,20,0,0,35,30,1,0,0,0,35,31,1,0,0,0,35,
        32,1,0,0,0,35,33,1,0,0,0,36,5,1,0,0,0,37,39,7,0,0,0,38,40,5,13,0,
        0,39,38,1,0,0,0,39,40,1,0,0,0,40,41,1,0,0,0,41,42,5,19,0,0,42,44,
        5,14,0,0,43,45,3,8,4,0,44,43,1,0,0,0,44,45,1,0,0,0,45,46,1,0,0,0,
        46,47,5,15,0,0,47,7,1,0,0,0,48,53,5,20,0,0,49,53,5,21,0,0,50,53,
        3,10,5,0,51,53,5,19,0,0,52,48,1,0,0,0,52,49,1,0,0,0,52,50,1,0,0,
        0,52,51,1,0,0,0,53,63,1,0,0,0,54,59,5,16,0,0,55,60,5,20,0,0,56,60,
        5,21,0,0,57,60,3,10,5,0,58,60,5,19,0,0,59,55,1,0,0,0,59,56,1,0,0,
        0,59,57,1,0,0,0,59,58,1,0,0,0,60,62,1,0,0,0,61,54,1,0,0,0,62,65,
        1,0,0,0,63,61,1,0,0,0,63,64,1,0,0,0,64,9,1,0,0,0,65,63,1,0,0,0,66,
        67,7,1,0,0,67,11,1,0,0,0,9,15,23,25,35,39,44,52,59,63
    ]

class btmlParser ( Parser ):

    grammarFileName = "btml_bracket.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'{'", "'}'", "'sequence'", "'selector'", 
                     "'fallback'", "'parallel'", "'act'", "'cond'", "'sub'", 
                     "'action'", "'condition'", "'subtree'", "'Not'", "'('", 
                     "')'", "','", "'True'", "'False'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "String", "Integer", 
                      "Float", "LINE_COMMENT", "WS" ]

    RULE_root = 0
    RULE_tree = 1
    RULE_internal_node = 2
    RULE_action_sign = 3
    RULE_action_parm = 4
    RULE_boolean = 5

    ruleNames =  [ "root", "tree", "internal_node", "action_sign", "action_parm", 
                   "boolean" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    String=19
    Integer=20
    Float=21
    LINE_COMMENT=22
    WS=23

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

        def EOF(self):
            return self.getToken(btmlParser.EOF, 0)

        def tree(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(btmlParser.TreeContext)
            else:
                return self.getTypedRuleContext(btmlParser.TreeContext,i)


        def getRuleIndex(self):
            return btmlParser.RULE_root

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRoot" ):
                listener.enterRoot(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRoot" ):
                listener.exitRoot(self)




    def root(self):

        localctx = btmlParser.RootContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_root)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 13 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 12
                self.tree()
                self.state = 15 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 120) != 0)):
                    break

            self.state = 17
            self.match(btmlParser.EOF)
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
            return self.getTypedRuleContext(btmlParser.Internal_nodeContext,0)


        def action_sign(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(btmlParser.Action_signContext)
            else:
                return self.getTypedRuleContext(btmlParser.Action_signContext,i)


        def tree(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(btmlParser.TreeContext)
            else:
                return self.getTypedRuleContext(btmlParser.TreeContext,i)


        def getRuleIndex(self):
            return btmlParser.RULE_tree

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTree" ):
                listener.enterTree(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTree" ):
                listener.exitTree(self)




    def tree(self):

        localctx = btmlParser.TreeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_tree)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 19
            self.internal_node()
            self.state = 20
            self.match(btmlParser.T__0)
            self.state = 25
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 8184) != 0):
                self.state = 23
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [7, 8, 9, 10, 11, 12]:
                    self.state = 21
                    self.action_sign()
                    pass
                elif token in [3, 4, 5, 6]:
                    self.state = 22
                    self.tree()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 27
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 28
            self.match(btmlParser.T__1)
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

        def Integer(self):
            return self.getToken(btmlParser.Integer, 0)

        def getRuleIndex(self):
            return btmlParser.RULE_internal_node

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInternal_node" ):
                listener.enterInternal_node(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInternal_node" ):
                listener.exitInternal_node(self)




    def internal_node(self):

        localctx = btmlParser.Internal_nodeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_internal_node)
        try:
            self.state = 35
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3]:
                self.enterOuterAlt(localctx, 1)
                self.state = 30
                self.match(btmlParser.T__2)
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 2)
                self.state = 31
                self.match(btmlParser.T__3)
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 32
                self.match(btmlParser.T__4)
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 4)
                self.state = 33
                self.match(btmlParser.T__5)
                self.state = 34
                self.match(btmlParser.Integer)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Action_signContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def String(self):
            return self.getToken(btmlParser.String, 0)

        def action_parm(self):
            return self.getTypedRuleContext(btmlParser.Action_parmContext,0)


        def getRuleIndex(self):
            return btmlParser.RULE_action_sign

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAction_sign" ):
                listener.enterAction_sign(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAction_sign" ):
                listener.exitAction_sign(self)




    def action_sign(self):

        localctx = btmlParser.Action_signContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_action_sign)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 8064) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 39
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==13:
                self.state = 38
                self.match(btmlParser.T__12)


            self.state = 41
            self.match(btmlParser.String)
            self.state = 42
            self.match(btmlParser.T__13)
            self.state = 44
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 4063232) != 0):
                self.state = 43
                self.action_parm()


            self.state = 46
            self.match(btmlParser.T__14)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Action_parmContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(btmlParser.Integer)
            else:
                return self.getToken(btmlParser.Integer, i)

        def Float(self, i:int=None):
            if i is None:
                return self.getTokens(btmlParser.Float)
            else:
                return self.getToken(btmlParser.Float, i)

        def boolean(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(btmlParser.BooleanContext)
            else:
                return self.getTypedRuleContext(btmlParser.BooleanContext,i)


        def String(self, i:int=None):
            if i is None:
                return self.getTokens(btmlParser.String)
            else:
                return self.getToken(btmlParser.String, i)

        def getRuleIndex(self):
            return btmlParser.RULE_action_parm

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAction_parm" ):
                listener.enterAction_parm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAction_parm" ):
                listener.exitAction_parm(self)




    def action_parm(self):

        localctx = btmlParser.Action_parmContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_action_parm)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 52
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [20]:
                self.state = 48
                self.match(btmlParser.Integer)
                pass
            elif token in [21]:
                self.state = 49
                self.match(btmlParser.Float)
                pass
            elif token in [17, 18]:
                self.state = 50
                self.boolean()
                pass
            elif token in [19]:
                self.state = 51
                self.match(btmlParser.String)
                pass
            else:
                raise NoViableAltException(self)

            self.state = 63
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==16:
                self.state = 54
                self.match(btmlParser.T__15)
                self.state = 59
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [20]:
                    self.state = 55
                    self.match(btmlParser.Integer)
                    pass
                elif token in [21]:
                    self.state = 56
                    self.match(btmlParser.Float)
                    pass
                elif token in [17, 18]:
                    self.state = 57
                    self.boolean()
                    pass
                elif token in [19]:
                    self.state = 58
                    self.match(btmlParser.String)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 65
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BooleanContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return btmlParser.RULE_boolean

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBoolean" ):
                listener.enterBoolean(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBoolean" ):
                listener.exitBoolean(self)




    def boolean(self):

        localctx = btmlParser.BooleanContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_boolean)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            _la = self._input.LA(1)
            if not(_la==17 or _la==18):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





