
parser grammar BTMLParser;

options {
    superClass = BTMLParserBase;
    tokenVocab = BTMLLexer;
}

root            : tree (NEWLINE | behavior_def)* EOF;

tree            : internal_node INDENT (behavior_sign | tree)* DEDENT;
internal_node   : (SEQUENCE | SELECTOR | PARALLEL) NEWLINE;
behavior_sign   : (ACT | COND) literal (AND literal)* NEWLINE;

literal         : String OPEN_PAREN behavior_parm? CLOSE_PAREN;
behavior_parm   : String (COMMA String)*;

behavior_def    : DEF (ACT | COND) literal ':' NEWLINE INDENT tree DEDENT;

