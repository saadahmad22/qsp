from .base_models import BaseTimeModel, time

class ClassSchedules(BaseTimeModel):

    def __init__(self) -> None:
        self.__vars__ =  {
        'stw_id' : int,
        'schedule_id' : int,
        'weekday' : str,
        'start_time' : time,
        'end_time' : time
        }
        BaseTimeModel.__init__(self)