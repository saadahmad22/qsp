from .base_models import BaseTimeModel, date

class Schedules(BaseTimeModel):

    def __init__(self) -> None:
        self.__vars__ =  {
        'schedule_id' : int,
        'class_id' : int,
        'teacher_id' : int,
        'start_date' : date,
        'end_date' : date,
        'price' : float,
        'digital_meeting_link' : str,
        'max_students' : int,
        'status' : str
        }
        BaseTimeModel.__init__(self)