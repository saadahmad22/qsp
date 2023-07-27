# 

from ..models.base_models import BaseTimeModel, date, time

class CourseCalendar(BaseTimeModel):

    def __init__(self) -> None:
        self.__vars__ = {
            "class_date" : date, 
            "start_time" : time, 
            "end_time" : time, 
            "notes" : str, 
            "status" : str, 
            "schedule_id" : int
        }
        BaseTimeModel.__init__(self)