from json import dumps

from ..models.base_models import BaseModel, BaseTimeModel
from .db_manager import DataBaseManager
from .enums import OrderType, LogicalOperator
from .oder_clause import OrderClause
from .relational_operator import RelationalOperator


class DataBaseHandler(DataBaseManager):

    def save(self, table_name : str, class_object : BaseModel) -> None:
        '''Saves the data in the class_object to the given sql table
        
        table_name : The str name of the SQL table
        class_object : The Python objects that models table_name (see above for table_name) and stores relevant data
        '''

        data = class_object.__vars__
        columns = ""
        values = ""
        questions = ""
        for key in tuple(data.keys())[1:]:
            columns += f'"{key}",'
            questions += "?,"
            values += f'"{str(data[key])}",'
            
        statement = f'INSERT INTO {table_name} ({columns[:-1]}) VALUES ({questions[:-1]})'
        if self.SHOW_SQL:
            print(f'INSERT INTO {table_name} ({columns[:-1]}) VALUES ({values[:-1]})')
        if self.SHOW_MODEL:
            print(dumps(class_object.__vars__))
        return_val = self.execute(statement, False, tuple(tuple(data.values())[1:]))
        return return_val

    def update(self, table_name : str, update_data : dict, operations: list):
        questions = ""
        for key, value in update_data.items():
            questions += f'{key} = ?,'

        where_clause = "WHERE "
        for operation in operations:
            where_clause += f'{operation.operand_a} {operation.operator.value} {operation.operand_b} {"" if not operation.logical_operator else operation.logical_operator.name} '

        statement = f'''UPDATE {table_name} SET {questions[:-1]} 
        {"" if not operations or len(operations) == 0 else  where_clause}'''

        if self.SHOW_SQL:
            print(statement)
        self.execute(statement, False, tuple(update_data.values()))

    def fetch_all(self, model : BaseModel, table_name : str, operations: list, order_by : list) -> list:
        fields_str = ""
        fields = model.__vars__.keys()
        for field in fields:
            fields_str += f"{field}, "
        args = []

        where_clause = "WHERE "

        for operation in operations:
            # check if literal. If it's not, then ? cannot be used
            #class_name = str(model.__class__.__name__).strip().lower()
            if not operation.operand_a_col:
                args.append(operation.operand_a)
                where_clause += " ? "
            else:
                where_clause += str(operation.operand_a)
            if not operation.operand_b_col:
                args.append(operation.operand_b)
                where_clause += f" {operation.operator.value} ? "
            else:
                where_clause += f' {operation.operator.value} {str(operation.operand_b)} '
            if operation.logical_operator:
                where_clause += f' {str(operation.logical_operator.name)} '

        order_by_str = "ORDER BY " 
        for col in order_by:
            order_by_str += f"{col.col} {col.type.name},"
            
        statement = f'''SELECT {fields_str[:-2]} FROM {table_name} {"" if not operations or len(operations) == 0 else where_clause} {"" if not order_by or len(order_by) == 0 else order_by_str[:-1]}'''
        db_results = self.execute(statement, True, args)

        # the list to return
        final_list = []
        for result in db_results:
            row_obj = type(model)()
            row_obj.init_from_data(data=result)
            final_list.append(row_obj)
        return final_list
    
    # def fetch_all(self, model : BaseModel, table_name : str) -> list:
    #     return self.fetch_all(model, table_name, [], [])
    
    def fetch(self, model : BaseModel, table_name : str, operations: list, order_by : list) -> None | BaseModel:
        return_val = self.fetch_all(model, table_name, operations, order_by)
        return None if len(return_val) < 1 else return_val[0]
    
    # def fetch(self, model : BaseModel, table_name : str) -> None | BaseModel:
    #     return_val = self.fetch_all(model, table_name, [], [])
    #     return None if len(return_val) < 1 else return_val[0]