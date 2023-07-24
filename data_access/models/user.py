from .base_models import BaseModel

class User(BaseModel):
    def __init__(self) -> None:
        self.__vars__ =  {
            'user_id' : int,
            'first' : str,
            'last' : str,
            'email' : str,
            'phone' : str,
            'password_hash ' : str,
            'role' : str
        }
        BaseModel.__init__(self)