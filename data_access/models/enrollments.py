from .base_models import BaseTimeModel, date

class Enrollments(BaseTimeModel):

    def __init__(self) -> None:
        self.__vars__ =  {
        'enrollment_id' : int,
        'user_id' : int,
        'schedule_id' : int,
        'enrollment_date' : date,
        'end_date' : date,
        'notes' : str,
        'status' : str
        }
        BaseTimeModel.__init__(self)