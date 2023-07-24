from .base_models import BaseTimeModel, date, time

class Calendar(BaseTimeModel):

    def __init__(self) -> None:
        self.__vars__ =  {
        'calendar_id' : int,
        'schedule_id' : int,
        'class_date' : date,
        'start_time' : time,
        'end_time' : time,
        'notes' : str,
        'status' : str
        }
        BaseTimeModel.__init__(self)