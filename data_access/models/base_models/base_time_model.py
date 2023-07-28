'''A base model for time-related classes
'''

from datetime import timedelta

from .base_model import BaseModel
from .converters import date, time, MIN_DATE, MIN_TIME, date_pattern, time_pattern, str_to_date, str_to_time


class BaseTimeModel(BaseModel):

    def __init_subclass__(cls) -> None:
        '''Append to the super subclass constructor to include date and time'''
        BaseTimeModel.__type_mappings__[date] = {"default_value" : MIN_DATE, "converter" : str_to_date}
        BaseTimeModel.__type_mappings__[time] = {"default_value" : MIN_TIME, "converter" : str_to_time}
        BaseModel.__init_subclass__()

    @staticmethod
    def in_between(start : date | time, end : date | time, test_time : date | time, inclusive=False) -> bool:
        # throw if class mismatch
        if not (start.__class__ == end.__class__ == test_time.__class__):
            this_class = BaseTimeModel.__class__
            type_issue_message = f'''
An error occurred in {this_class.__module__}.{this_class.__name__}
Note that start, end, and test_time values must be all of either datetime.date or datetime.time'''
            raise TypeError(type_issue_message)
        # throw if start comes after end
        elif start > end:
            this_class = BaseTimeModel.__class__
            raise ValueError(f"An error occurred in {this_class.__module__}.{this_class.__name__}. The start value is greater than the end value")
        # return true if its actually in the middle, otherwise false
        return start <= test_time <= end if inclusive else start < test_time < end
    
    @staticmethod
    def date_str(date_obj : date) -> str: 
        # if error, throw. else, return val
        if not isinstance(date_obj, date):
            this_class = BaseTimeModel.__class__
            error_message = f"An error occurred in {this_class.__module__}.{this_class.__name__}. {date_obj} cannot be converted to type str because it is not a datetime.date object"
            raise ValueError(error_message)
        return date_obj.strftime(date_pattern["datetime"])
    
    @staticmethod
    def time_str(time_obj : time) -> str:
        # if error, throw. else, return val
        if not isinstance(time_obj, time):
            this_class = BaseTimeModel.__class__
            error_message = f"An error occurred in {this_class.__module__}.{this_class.__name__}. {time_obj} cannot be converted to type str because it is not a datetime.time object"
            raise ValueError(error_message)
        return time_obj.strftime(time_pattern['datetime'])
    
    @staticmethod
    def time_equals(time_obj_a : time, time_obj_b : time):
        if not isinstance(time_obj_a, time) or not isinstance(time_obj_b, time):
            this_class = BaseTimeModel.__class__
            error_message = f"An error occurred in {this_class.__module__}.{this_class.__name__}. {time_obj_a} or {time_obj_b} cannot be compared because they are not both datetime.time objects"
            raise ValueError(error_message)
        return time_obj_b.minute == time_obj_a.minute and time_obj_a.hour == time_obj_b.hour
    
    @staticmethod
    def date_range(start_date, end_date):
        for n in range(int((end_date - start_date + timedelta(days=1)).days)):
            yield start_date + timedelta(n)