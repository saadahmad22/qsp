'''Models a mathematical operation'''

from .enums import LogicalOperator
from .relational_operator import RelationalOperator

class Operation:
    operand_a : str
    operand_b : str
    operator : RelationalOperator
    logical_operator : LogicalOperator
    def __init__(self, operand_a : str, operand_b : str, operator : RelationalOperator, logical_operator : LogicalOperator=None, operand_a_col : bool=False, operand_b_col : bool=False ) -> None:
        '''Models an SQL operation (in a WHERE clause)
        
        operand_a : left-hand side of the SQL clause
        operand_b : right-hand side of the SQL clause
        operator : an enum of RelationalOperator which is the operator of the clause (e.g., >=, ==, etc.)
        operand_a_col : True if @operand_a is an SQL column (the internals work differently)
        operand_b_col : True if @operand_b is an SQL column (the internals work differently)
        '''
        self.operand_a = operand_a
        self.operand_b = operand_b
        self.operator = operator
        self.logical_operator = logical_operator
        self.operand_a_col = operand_a_col
        self.operand_b_col = operand_b_col