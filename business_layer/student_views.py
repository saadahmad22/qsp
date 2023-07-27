import sys

from flask import flash, redirect, render_template, request, session, url_for
from json import dumps

# append the path of the parent directory
sys.path.append("..")

from data_access.db import DataBaseHandler, Operation, RelationalOperator, OrderClause, OrderType
from data_access.views import CourseCalendar, MyCourses
from .forms import StdHomePage

db_handler = DataBaseHandler()

def do_student_home_page():
    '''Code to generate a dashboard for the student'''
    form = StdHomePage(request.form)

    if request.method == "GET":
        #---------fetch the enrolled schedules------------
        # fetches all classes where the user is enrolled in (active & inactive)
        enrolled_schedules = DataBaseHandler().fetch_all(MyCourses(), "my_courses_view", 
            [Operation("user_id", session.get("user_id"), RelationalOperator.EQ, operand_a_col=True)], 
            [OrderClause("schedule_id", OrderType.ASC)])
        
        #---------format data for jinja------------
        # sends relevant data to 'form', which constructs the select field
        form.selected_class.choices = [(-1, "Select Class")] 
        # populate the variables above with data from every schedule pulled
        for schedule in enrolled_schedules:
            form.selected_class.choices.append((schedule.get("schedule_id"), f'{schedule.get("title")} with {schedule.get("first")} {schedule.get("last")}'))
        num_schedules = len(enrolled_schedules)
        # To Convert python json to js json: const json_data = JSON.parse({{#schedules_json|tojson|safe}});
        
        if num_schedules == 1:
            session["class_id"] = enrolled_schedules[0].get("schedule_id")
            return redirect(url_for('student_classes_view'))
        return render_template("student_home.html", form=form, 
                num_schedules=len(enrolled_schedules), selected_class=-1)
    else:
        '''
        # temp var to send form data to js on other end
        temp_json_dict = {} 
        
        for schedule in enrolled_schedules:
            temp_json_dict[str(schedule.get("schedule_id"))] = {field : str(value) for field, value in schedule.__vars__.items()}
        schedules_json = dumps(temp_json_dict)
        '''
    return "Hi"