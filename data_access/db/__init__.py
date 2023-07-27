'''This is the main module of sql, which handles everything pretaining to the database

This module initializes the database upon import. 
Then execute() can be called to run sql code.
A convinience method called convert_time() is provided to help manage time object management

Usage:
    You can use this module as follows:

    >>> from data.sql import DataManager
    >>> ...
    >>> build the flask app
    >>> ...
    >>> 
    >>> db = DataManager()
    >>> ...rest of code using db at will...

Functions:
    execute(statement : str, *args) -> None | dict: it will run the SQL code and pass any provided parameters.
        it will return None or a dict of the query, depending on the SQL given
        
'''

# imports
from .db_handler import DataBaseHandler
from .enums import OrderType, LogicalOperator
from .oder_clause import OrderClause
from .relational_operator import RelationalOperator
from .operation import Operation
from .table_fetchers import fetch_user



__all__ = ["DataBaseHandler", "LogicalOperator", "OrderType", "OrderClause", "RelationalOperator", "Operation", "fetch_user"]