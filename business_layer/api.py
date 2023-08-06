import sys
from json import dumps
from flask import redirect, flash, request, session

sys.path.append("..")

from data_access.db import (DataBaseHandler, Operation, RelationalOperator, OrderClause, OrderType)
from data_access.models import Schedules, ClassSchedules
from data_access.models.base_models import date, timedelta
from data_access.views import CourseCalendar, CalendarInfo, MyCourses, Payments

def do_error():
    '''Flashes the desired message and redirects to the desired url'''

    error_json = request.get_json()
    flash(f'''{error_json["message"]}
{error_json["error_message"]}''')
    return redirect(request.get_json()["url"])

def do_get_calendar(schedule_id : int, month_id : str=None):
    '''Returns the JSON required to construct student home page calendar
    
    JSON structure
    {
        - Schedules fields in top level
        - include schedule_id, class_id, teacher_id,
            start_date, end_date, price, digital_meeting_link, max_students, status
        - title, desc, teacher full name ("name"), schedule_id
        - "generic_days" : [
            weekday : {
                start_time : 24-hour HH:MM, 
                end_time : 24-hour HH:MM
            }
        ]
        - "days" : list of all the required calendar dates [
            -  "month_id" : {
                first_day : <of month> (Monday = 0)
                YYYY-MM-DD : {
                    either {status: 'inactive'} or a fully mapped @CourseCalendar object
                }
            }
        ]

    }
    '''

    db_handler = DataBaseHandler()

    # convenience operator to check that the schedule_id column matches input
    schedule_op = Operation("schedule_id", schedule_id, RelationalOperator.EQ, operand_a_col=True)
    # load the class, else throw an HTTP error
    try :
        view = db_handler.fetch(Schedules(), "schedules", [schedule_op], [])
    except Exception:
        return "Class not found", 400 
    
    # fetch and sort the schedule's calendar. NOTE: there will be empty dates that need to be handled front end
    days = db_handler.fetch_all(CourseCalendar(), "course_calendar_view", [schedule_op], [])  
    days.sort(key=lambda day : day.get("class_date"))  

    # fetch extra calendar info
    calendar_info = db_handler.fetch(CalendarInfo(), "calendar_info", [schedule_op], [])

    # loop through every day in days and organize them into a month
    class_start = view.get("start_date") if not month_id else date(int(month_id[2:]), int(month_id[:2]), 1)
    next_ = (class_start + timedelta(days=31))
    prev_ = (class_start - timedelta(days=3))
    # fill up month
    first_day = class_start.replace(day=1)
    temp_day = first_day
    weeks = 0
    months = [f'{str(first_day.month).zfill(2)}{first_day.year}']
    while temp_day.month == first_day.month:
        weeks += 1
        temp_day += timedelta(days=7)
    month = {
        "first_day" : first_day.weekday(), 
        "last_day" : ((first_day.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)).day,
        "weeks" : weeks, 
        "name" : first_day.strftime("%B"), 
        "year" : first_day.year,
        "id" : f'{str(first_day.month).zfill(2)}{first_day.year}',
        "next" : {"is_class" : False, "id" :f'{str(next_.month).zfill(2)}{next_.year}' },
        "prev" : {"is_class" : False, "id" :f'{str(prev_.month).zfill(2)}{prev_.year}' },
        }
    for day in days:
        a_day = day.get("class_date")
        if eq_month_year(a_day, class_start):
            month[day.get("class_date").day] = {field : str(val) for field, val in day.__vars__.items()}
        else:
            id_ = f'{str(a_day.month).zfill(2)}{a_day.year}'
            if id_ not in months:
                months.append(id_)
                if eq_month_year(a_day, next_):
                    month["next"]["is_class"] = True
                elif eq_month_year(a_day, prev_):
                    month["prev"]["is_class"] = True
            
                

    # load data to a dict b/c original classes aren't serializable
    schedule_json = {key : str(val) for key, val in view.__vars__.items()}
    schedule_json["month"] = month
    schedule_json["months"] = months
    schedule_json["generic_days"] = [
            {
            "weekday"  : {
            "start" : str(weekday.get("start_time")),
            "end" : str(weekday.get("end_time")),
            "name" : weekday.get("weekday")
            }
        }
        for weekday in db_handler.fetch_all(ClassSchedules(), "class_schedules", [schedule_op], [])
        ]
    schedule_json.update({
        "title" : calendar_info.get("title"),
        "desc" : calendar_info.get("description"),
        "name" : calendar_info.get("first") + " " + calendar_info.get("last")
        })

    return dumps(schedule_json)

def eq_month_year(date1 : date, date2 : date) -> bool:
    return isinstance(date1, date) and isinstance(date2, date) and  date1.month == date2.month and date1.year == date2.year

def do_get_payments():
    enrolled_schedules = DataBaseHandler().fetch_all(Payments(), "payments_view", 
        [Operation("user_id", session.get("user_id"), RelationalOperator.EQ, operand_a_col=True)], [])
    enrolled_schedules.sort(key=lambda day : day.get("pay_to_date"), reverse=True)
    payments_json = []
    for payment in enrolled_schedules:
        match payment.get("paid"):
            case "TRUE":
                payment.__vars__["paid"] = "Yes"
            case _:
                payment.__vars__["paid"] = "No"
        payment.__vars__["date_paid"] = "--" if not payment.get("date_paid") or payment.get("date_paid") == date(1, 1, 1) else payment.date_str(payment.get("date_paid"))
        payment.__vars__["pay_from_date"], payment.__vars__["pay_to_date"] =  map(payment.date_str, 
            (payment.get("pay_from_date"), payment.get("pay_to_date"))) 
        
        payment.__vars__["title"] += f' with {payment.get("first")} {payment.get("last")}'
        payment.__vars__["amount"] = f'${float(payment.get("amount"))}'
        del(payment.__vars__["first"])
        del(payment.__vars__["last"])
        payments_json.append({field : str(val) for field, val in payment.__vars__.items()})
    return dumps(payments_json)
