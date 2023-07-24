import sqlite3 as sql

from .config import configs

class DataBaseManager:
    DB_LOC = configs["DB_LOC"]
    SHOW_SQL = configs["SHOW_SQL"]
    SHOW_MODEL = configs["SHOW_MODEL"]

    def commit_changes(self, connection : sql.Cursor):
        connection.commit()
    
    def execute(self, statement : str, read_only : bool = True, *args) -> tuple | None :
        '''Takes in a string sql statement and an unknown number of parameters. The it executes it on the database'''

        connection = sql.connect(self.DB_LOC)
        data = connection.execute(statement, *args).fetchall()
        if not read_only:
            self.commit_changes(connection)
        connection.close()
        return data
