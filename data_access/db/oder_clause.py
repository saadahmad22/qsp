'''Structure to generate sql WHERE clause'''

from .enums import OrderType

class OrderClause:
    type : OrderType
    col : str

    def __init__(self, col : str, type: OrderType) -> None:
        self.type = type
        self.col = col