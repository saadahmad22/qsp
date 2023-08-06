from ..models.base_models import BaseTimeModel, date

class Payments(BaseTimeModel):

    def __init__(self) -> None:
        self.__vars__ = {
            "user_id"  : int,
            'title' : str,
            'first' : str,
            'last' : str,
            'amount' : int,
            'paid' : str,
            'date_paid' : date,
            'pay_from_date' : date,
            'pay_to_date' : date
        }
        self.days = None
        BaseTimeModel.__init__(self)