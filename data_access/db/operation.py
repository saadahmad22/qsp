'''Models a mathematical operation'''

from .enums import LogicalOperator
from .relational_operator import RelationalOperator

class Operation:
    operand_a : str
    operand_b : str
    operator : RelationalOperator
    logical_operator : LogicalOperator
    def __init__(self, operand_a : str, operand_b : str, operator : RelationalOperator, logical_operator : LogicalOperator=None) -> None:
        self.operand_a = operand_a
        self.operand_b = operand_b
        self.operator = operator
        self.logical_operator = logical_operator