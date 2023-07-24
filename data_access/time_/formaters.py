from . import dt

def format_for_sql(datetime_instance : dt) -> str:
    '''Turns a datetime object into a string compatible with sqlite'''
    return datetime_instance.isoformat(' ')[:19]

def convert_iso_to_dt(time : str) -> dt:
    return dt.fromisoformat(time)