from antlr4 import *

class BTMLParserBase(Parser):

    def CannotBePlusMinus(self) -> bool:
        return True

    def CannotBeDotLpEq(self) -> bool:
        return True
