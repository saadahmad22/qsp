from .base_models import BaseModel

class Teachers(BaseModel):
    def __init__(self) -> None:
        self.__vars__ =  {
            'teacher_id' : int,
            'first' : str,
            'last' : str,
            "qualification" : str,
            'status' : str
        }
        BaseModel.__init__(self)