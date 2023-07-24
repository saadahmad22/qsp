'''Methods that convert string to the desired class'''
from datetime import datetime

from .testers import date, time, is_date, is_time, is_bool, date_pattern, time_pattern

# error values for date and time, in case something goes wrong
MIN_DATE = date(1, 1, 1)
MIN_TIME = time(0, 0, 0)

def str_to_bool(bool_val) -> bool:
    bool_val_type = is_bool(bool_val)
    if bool_val_type == None:
        raise ValueError(f"The object {str(bool_val)} cannot be converted to a boolean because it is not in a string or boolean format")
    try:
        match bool_val_type:
            case int():
                return bool_val == 1
            case bool():
                return bool_val
            case str():
                return str(bool_val).lower().strip() in ["true", "1"]
            case _:
                raise ValueError(f"An unknown error occurred while converting {bool_val} to a boolean")
    except Exception as error:
        raise ValueError(f'''The object {str(bool_val)} cannot be converted to a boolean because a system error ocurred
            {error}''')

def str_to_date(date_value : str) -> date:
    '''Takes a string in as MM/DD/YYYY and returns the date object'''

    if not is_date(date_value):
        if str(date_value) != "":
            error_message = f"{date_value} cannot be converted to a datetime.date object because it is not in the following format: '{date_pattern['text']}'"
            raise ValueError(error_message)
        return MIN_DATE
    return datetime.strptime(str(date_value), date_pattern["datetime"]).date()

def str_to_time(time_value : str) -> time:
    '''Takes a string in as HH:MM and returns the naive time object'''
    
    # if error, throw. else, return val
    if not is_time(time_value):
        if  str(time_value) != "":
            error_message = f"{time_value} cannot be converted to a datetime.time object because it is not in the following format: '{time_pattern['text']}'"
            raise ValueError(error_message)
        return MIN_TIME
    return datetime.strptime(str(time_value), time_pattern['datetime']).time() 