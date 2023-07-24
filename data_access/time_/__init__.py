''' NOTE: THIS MODULE IS DEPRECATED. functionality is available in models -> base models (might get moved later)
This module containes convinience functions to handle time management

Functions:
    current_time() -> datetime.datetime: 
        fetches the current time in CST
    format_for_sql(datetime_instance : tuple) -> tuple:
      Takes a datetimeobject and returns in as a string compatible with sqlite
      This is in the format "YYYY-MM-DD HH:MM:SS"
    def convert_time(datetime_instance : dt) -> tuple:
        Converted the time into CST
        
'''

#imports
from datetime import datetime as dt
import pytz as tz
from calendar import Calendar, month_name
from .formaters import format_for_sql, convert_iso_to_dt
from .converters import convert_time, naive_to_aware

__all__ = ['format_for_sql', 'convert_iso_to_dt', 'MIN_DT', 'convert_time',
'current_time', 'create_dt', 'generate_calendar', 'month_date_year', 'naive_to_aware',
'get_hour_minute']

MIN_DT =  dt(1883, 1, 1, 0, 0, 0, 0, tzinfo=tz.timezone('America/Chicago'))

cal = Calendar(firstweekday=6)

#functions

def current_time() -> dt:
    val = dt.now(tz.timezone('US/Central')) 
    val = val.replace(microsecond=0)
    return val

def create_dt(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=tz.timezone('US/Central'), *, fold=0) -> dt:
    return dt(year, month, day, hour=hour, minute=minute, second=second, microsecond=microsecond, tzinfo=tzinfo, fold=fold)

def month_date_year(date : dt) -> tuple:
    return (month_name[date.month], date.day, date.year)

def get_hour_minute(date : dt) -> list:
    '''Returns the datetimes in the following form: Weekday name, day_in_month number, weekday number [0-6], hour, am/pm, minute'''
    return date.strftime("%A;%w;%d;%I;%p;%M").split(";")

def generate_calendar(day_in_month : dt) -> list:
    '''Returns a 2-d list of all the dates in the month

    makes a calendar in the following format:
      list_month( list_week( (day_of_month, day_of_week) ), list_week(), ...)
    '''
    # only does the start date for now
    
    return cal.monthdayscalendar(day_in_month.year, day_in_month.month)

#def generate_schedules(start : dt, end : dt, weekday : str):
    # monthdays2calendar
