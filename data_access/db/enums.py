'''Defines enums for use in the module
- LogicalOperator
    - Conjunctive phrases in sql
- OrderType
    - Where clause order by 
'''

from enum import Enum

LogicalOperator = Enum('LogicalOperator', ['AND', 'OR', 'NOT'])

OrderType = Enum("OrderType", ["ASC", "DESC"])