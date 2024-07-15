
parser grammar BTMLParser;

options {
    superClass = BTMLParserBase;
    tokenVocab = BTMLLexer;
}


//root            : EOF;
root            : tree+ EOF;
tree            : internal_node NEWLINE (INDENT (action_sign | tree)+ DEDENT)?;
internal_node   : SEQUENCE | SELECTOR | PARALLEL;
action_sign     : (ACT | COND) NOT? String OPEN_PAREN action_parm? CLOSE_PAREN NEWLINE;
action_parm     : (String) (COMMA (String))*;
