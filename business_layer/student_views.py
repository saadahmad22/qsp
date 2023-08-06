import sys

from flask import render_template, request, session

# append the path of the parent directory
sys.path.append("..")

from configs import NAVBAR

from data_access.db import DataBaseHandler, Operation, RelationalOperator, OrderClause, OrderType
from data_access.views import MyCourses
from .forms import StdHomePage

db_handler = DataBaseHandler()

def do_payments():
    return render_template("payments.html", navbar=NAVBAR)

def do_student_home_page():
    '''Code to generate a dashboard for the student'''
    form = StdHomePage(request.form)
    #---------fetch the enrolled schedules------------
    # fetches all classes where the user is enrolled in (active & inactive)
    enrolled_schedules = DataBaseHandler().fetch_all(MyCourses(), "my_courses_view", 
        [Operation("user_id", session.get("user_id"), RelationalOperator.EQ, operand_a_col=True)], 
        [OrderClause("schedule_id", OrderType.DESC)])
    
    #---------format data for jinja------------
    # sends relevant data to 'form', which constructs the select field
    form.selected_class.choices = [] 
    # populate the variables above with data from every schedule pulled
    for schedule in enrolled_schedules:
        form.selected_class.choices.append((schedule.get("schedule_id"), f'{schedule.get("title")} with {schedule.get("first")} {schedule.get("last")}'))
    num_schedules = len(enrolled_schedules)

    return render_template("student_home.html", form=form, 
            num_schedules=num_schedules, selected_class=-1, navbar=NAVBAR)