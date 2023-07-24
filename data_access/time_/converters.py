from . import dt
from . import tz

def convert_time(datetime_instance : dt) -> dt:
    '''Takes a datetime object and returns it in CST'''

    copy_dt = datetime_instance.astimezone(tz.timezone('America/Chicago'))
    return copy_dt

def naive_to_aware(date : dt) -> dt:
    '''Converts a naive dt to an aware one in the correct timezone'''

    return date if date.tzinfo is not None else tz.timezone('America/Chicago').localize(date)