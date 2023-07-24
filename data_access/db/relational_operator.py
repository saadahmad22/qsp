'''Maps Relational Operators to their SQL representations. Inherits properties and methods from Python's Enum class'''

from .enums import Enum

class RelationalOperator(Enum):
    LT = '<'
    GT = '>'
    EQ = "=="
    LE = '<='
    GE = '>='
    NE = '!='