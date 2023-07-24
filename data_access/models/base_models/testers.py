'''Check if a value is of a specified type'''

from datetime import date, time
from re import match

from .patterns import date_pattern, time_pattern


def is_date(date_val : date | str) -> bool:
    return isinstance(date_val, date) or (isinstance(date_val, str) and match(date_pattern["regex"], date_val))

def is_time(time_val : time | str) -> bool:
    return isinstance(time_val, time) or (isinstance(time_val, str) and match(time_pattern["regex"], time_val))

def is_bool(bool_val : bool | int | str) -> type:
    if isinstance(bool_val, int) and bool_val != 1 and bool_val != 0:
        return int
    elif isinstance(bool_val, bool):
        return bool
    elif isinstance(bool_val, str):
        allowed_bool_vals = ("false", "0", "true", "1")
        bool_val = str(bool_val).lower().strip()
        return bool if bool_val in allowed_bool_vals else None
    return None