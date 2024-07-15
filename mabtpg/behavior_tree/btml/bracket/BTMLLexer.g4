
lexer grammar BTMLLexer;

tokens {
    INDENT,
    DEDENT
}

options {
    superClass = BTMLLexerBase;
}

NEWLINE: ({self.atStartOfInput()}? SPACES | ( '\r'? '\n' | '\r' | '\f') SPACES?) {self.onNewLine();};

OPEN_PAREN         : '(';
CLOSE_PAREN        : ')';
COMMA              : ',';

//NEWLINE         : '\r'? '\n' | '\r' | '\f' SPACES? { self.handleNewLine() };
SPACES          : [ \t]+ -> channel(HIDDEN);

LINE_COMMENT    : '//' .*? '\r'? '\n' -> skip;
WS              : [ \t\u000C\r\n]+ -> skip;

SEQUENCE        : 'sequence';
SELECTOR        : 'fallback' | 'selector';
PARALLEL        : 'parallel';
ACT             : 'action' | 'act';
COND            : 'condition' | 'cond';
NOT             : 'Not';

String          : [a-zA-Z_][a-zA-Z_0-9]*;

COLON           : ':';
