from .base_models import BaseTimeModel, date

class Payments(BaseTimeModel):

    def __init__(self) -> None:
        self.__vars__ =  {
        'payment_id' : int,
        'enrollment_id' : int,
        'amount' : int,
        'paid' : bool,
        'date_paid' : date,
        'pay_from_date' : date,
        'pay_to_date' : date
        }
        BaseTimeModel.__init__(self)