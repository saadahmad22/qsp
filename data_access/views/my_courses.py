from ..models.base_models import BaseTimeModel, date

class MyCourses(BaseTimeModel):

    def __init__(self) -> None:
        self.__vars__ = {
            "user_id"  : int,
            "schedule_id" : int,
            "enrollment_date" : date,
            'end_date' : date,
            'class_id' : int,
            'title' : str,
            'description' : str,
            'status' : str,
            'first' : str, # teacher's first name
            'last' : str # teacher's last name
        }
        self.days = None
        BaseTimeModel.__init__(self)