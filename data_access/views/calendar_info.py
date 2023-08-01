from ..models.base_models import BaseModel 

class CalendarInfo(BaseModel):

    def __init__(self) -> None:
        self.__vars__ = {
            "class_id" : int, 
            "title" : str, 
            "description" : str, 
            "first" : str,
            "last" : str, 
            "schedule_id" : int,
        }
        BaseModel.__init__(self)