
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
OPEN_BRACE         : '{';
CLOSE_BRACE        : '}';


//NEWLINE         : '\r'? '\n' | '\r' | '\f' SPACES? { self.handleNewLine() };
//SPACES          : [ \t]+ -> channel(HIDDEN);


LINE_COMMENT    : '//' .*? '\r'? '\n' -> skip;
//WS              : [ \t\u000C\r\n]+ -> skip;
WS              : [ \t]+ -> skip; // Skip whitespace

SEQUENCE        : 'sequence' | 'seq';
SELECTOR        : 'fallback' | 'selector' | 'fal' | 'sel';
PARALLEL        : 'parallel';
ACT             : 'action' | 'act' | 'subtree' | 'sub';
COND            : 'condition' | 'cond';
NOT             : 'Not';

String          : [a-zA-Z0-9_-]+;

COLON           : ':';

DEF           : 'def' SPACES ;
AND           : SPACES ('&' | 'and');


fragment SPACES: [ \t]+;