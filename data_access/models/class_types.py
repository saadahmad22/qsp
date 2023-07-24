from .base_models import BaseModel

class ClassTypes(BaseModel):
    def __init__(self) -> None:
        self.__vars__ =  {
            'class_id' : int,
            'title' : str,
            'description' : str,
            'status' : str
        }
        BaseModel.__init__(self)