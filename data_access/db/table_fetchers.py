from . import DataBaseHandler, LogicalOperator, Operation, RelationalOperator
from ..models import User

db_handler = DataBaseHandler()

def fetch_user(email : str="", user_id : str="") -> User | None:
    '''Returns a list of Users (fetched from the db) from the data retrieved in login_form
    
    NOTE: either email or user_id must be given'''

    try:
        if not email or email == "":
            search_args = Operation("user_id", f'{str(user_id)}', RelationalOperator.EQ, operand_a_col=True)
        else:
            search_args = Operation("email", f'{str(email)}', RelationalOperator.EQ, operand_a_col=True)
        return db_handler.fetch(User(), "users", [search_args], [])
    except Exception:
        return None

