# # from helpers.sql import execute
# # from json import dumps
# from enum import Enum
# import os

# from data_access.models import User

# # print(os.getcwd())
# from data_access.db import DataBaseHandler, Operation, RelationalOperator

# db_handler = DataBaseHandler()
# search_args = Operation("users.email", 'saadahmad9@outlook.com', RelationalOperator.EQ)

# print(db_handler.fetch(User(), "users", [search_args], []))




# my_teacher = Teachers()
# my_teacher.init_from_data(('100', 'Moaz', 'Abid', 'Egyption school', 'active'))
# my_teacher.__vars__["teacher_id"] = 102

# print(db_handler.save("teachers", my_teacher))

# # from .db import DataBaseManager
# from data_access.db import DataBaseHandler

# db_handler = DataBaseHandler()    

# print(RelationalOperator.LT.value)

# def save(table_name:str, class_object):
#     print(dumps(class_object.__dict__))
#     data = class_object.__dict__
#     columns = ""
#     values = ""
#     questions = ""
#     for key in data.keys():
#         columns += f'"{key}",'
#         questions += "?,"
#         values += f'"{data[key]}",'
        
#     statement = f'INSERT INTO {table_name} ({columns[:-1]}) VALUES ({questions[:-1]})'
#     if (show_sql):
#         print(f'INSERT INTO {table_name} ({columns[:-1]}) VALUES ({values[:-1]})')
    

#     return execute(statement, tuple(data.values()))

# def update(table_name : str, update_data : dict, operations: list):
#     questions = ""
#     for key, value in update_data.items():
#         questions += f'{key} = ?,'

#     where_clause = "WHERE "
#     for operation in operations:
#         where_clause += f'{operation.operand_a} {operation.operator.value} {operation.operand_b} {"" if not operation.logical_operator else operation.logical_operator.name} '

#     statement = f'UPDATE {table_name} SET {questions[:-1]} {where_clause}'
#     print(statement)
#     execute(statement, tuple(update_data.values()))

# def fetch_all(model, table_name : str, operations: list, order_by : list):
#     fields_str = ""
#     fields = model.__dict__.keys()
#     for field in fields:
#         fields_str += f"{field}, "

#     where_clause = "WHERE "
#     for operation in operations:
#         where_clause += f'{operation.operand_a} {operation.operator.value} {operation.operand_b} {"" if not operation.logical_operator else operation.logical_operator.name} '

#     order_by_str = "ORDER BY " 
#     for col in order_by:
#         order_by_str += f"{col.col} {col.type.name},"
        
#     statement = f'''SELECT {fields_str[:-2]} FROM {table_name} 
#         {"" if not operations or len(operations) == 0 else where_clause} 
# {"" if not order_by or len(order_by) == 0 else order_by_str[:-1]}'''
#     results = execute(statement)
#     return [type(model)(result) for result in results]
    
# def fetch(model, table_name : str, operations: list, order_by : list):
#     return_val = fetch_all(model, table_name, operations, order_by)
#     return [] if len(return_val) < 1 else return_val[0]

    


# my_user = User()
# my_user.user_id = 10001
# my_user.first = "first"
# my_user.last = "last"
# my_user.email = "my_email"
# my_user.phone = "111-111-1111"
# my_user.password_hash = "my_hash"
# my_user.role = "student"

# #save("users", my_user)
# operation1 = Operation("user_id", 10001, RelationalOperator.EQ, logical_operator=LogicalOperator.AND)
# operation2 = Operation("email", '"my_email"', RelationalOperator.EQ)
# order_clause = OrderClause("email", OrderType.DESC)

# #update("users", {"first" : "my_name"}, [operation1, operation2])
# print(fetch_all(User(), "users", [operation1, operation2], [order_clause]))