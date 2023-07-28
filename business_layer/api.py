import sys
from json import dumps

sys.path.append("..")

from data_access.db import (DataBaseHandler, Operation, RelationalOperator)
from data_access.models import Schedules
from data_access.models.base_models import date, timedelta
from data_access.views import CourseCalendar


def do_get_calendar(schedule_id):
    '''Returns the JSON required to construct student home page calendar
    
    JSON structure
    {
        - Schedules fields in top level
        - include schedule_id, class_id, teacher_id,
            start_date, end_date, price, digital_meeting_link, max_students, status
        - "DAYS" : list of all the required calendar dates
            -  "monthid" : {
                    first_day : <of month> (Monday = 0)
                    YYYY-MM-DD : {
                        either {class_date: '2023-08-01', status: 'inactive'}
                    }
                }
    }

    '''

    # convenience operator to check that the schedule_id column matches input
    schedule_op = Operation("schedule_id", schedule_id, RelationalOperator.EQ, operand_a_col=True)
    # load the class, else throw an HTTP error
    try :
        view = DataBaseHandler().fetch(Schedules(), "schedules", [schedule_op], [])
    except Exception:
        return "Class not found", 400 
    # fetch and sort the schedule's calendar. NOTE: there will be empty dates that need to be filled up as such 
    days = DataBaseHandler().fetch_all(CourseCalendar(), "course_calendar_view", [schedule_op], [])  
    days.sort(key=lambda day : day.get("class_date"))  
    # loop through every day between the class's start and end, then populate the empty days
    # at the same time, organize all days into a month
    start_date = view.get("start_date") # convenience fetch to save cpu
    start = date(start_date.year, start_date.month, 1) # start date
    end_date = view.get("end_date")  # convenience fetch to save cpu
    end = (end_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1) # end date
    days_fetched = [day.get("class_date") for day in days] # days already present
    i = 0 # index of number of days in from the schedule's start month to the end month 
    months = {}
    for a_day in Schedules.date_range(start, end):
        if a_day not in days_fetched:
            days.insert(i, {"status" : "inactive"})
        month_id = f'{str(a_day.month).zfill(2)}{a_day.year}'
        if a_day.day == 1: # put one time code for the month here as well
            months[month_id] = {"first_day" : a_day.weekday()}
        months[month_id][str(a_day)] = {field : str(val) for field, val in (days[i].__vars__.items() if isinstance(days[i], CourseCalendar) else days[i].items())}
        i += 1
    # load data to a dict b/c original classes aren't serializable
    schedule_json = {key : str(val) for key, val in view.__vars__.items()}
    schedule_json["DAYS"] = months

    return dumps(schedule_json)