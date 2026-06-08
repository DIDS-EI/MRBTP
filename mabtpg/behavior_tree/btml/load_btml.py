import os
from antlr4 import *
import tempfile
from pprint import pprint

from mabtpg.behavior_tree.btml.BTMLListener import BTMLListener
from mabtpg.behavior_tree.btml.grammar.BTMLLexer import BTMLLexer
from mabtpg.behavior_tree.btml.grammar.BTMLParser import BTMLParser


def load_btml(btml_path: str, verbose =False):
    """_summary_

    Args:
        btml_path (str): _description_
        behaviour_lib_path (str): _description_

    Raises:
        FileNotFoundError: _description_
        FileNotFoundError: _description_
    """
    # error handle
    # if not os.path.exists(btml_path):
    #     raise FileNotFoundError("Given a fault btml path: {}".format(btml_path))

    # noting fault, go next
    # with tempfile.NamedTemporaryFile(mode='w',delete=False) as tmp_file:
    #     format_trans_to_bracket(btml_path, tmp_file)
    #     tmp_file_path = tmp_file.name

    # input_stream = FileStream(btml_path, encoding="utf-8")
    # os.remove(tmp_file_path)

    input_stream = FileStream(btml_path, encoding="utf-8")

    lexer = BTMLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    if verbose:
        stream.fill()
        tokens = stream.tokens
        for token in tokens:
            token_type = lexer.symbolicNames[token.type] if token.type > 0 else "EOF"
            print(f"Type: {token_type}, Text: '{token.text}', Line: {token.line}, Column: {token.column}")

    parser = BTMLParser(stream)
    tree = parser.root()

    if verbose:
        # print(getIndentedTreeString(tree, parser))
        print(tree.toStringTree(recog=parser))

    walker = ParseTreeWalker()

    btml_listener = BTMLListener()  # listener mode
    walker.walk(btml_listener, tree)

    return btml_listener.btml
