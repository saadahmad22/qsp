from os import urandom as generate_secret_key
from tempfile import gettempdir

from flask import Flask, flash, redirect, render_template, url_for
from flask_wtf.csrf import CSRFProtect
from passlib.apps import custom_app_context as pwd_context

from configs import NAVBAR

from business_layer.api import do_error, do_get_calendar, do_get_payments
from business_layer.login_manager import (do_login, do_logout, do_register,
                                          student_login_required)
from business_layer.student_views import do_payments, do_student_home_page
from flask_session import Session

# create and configure the app/jinja environment
app = Flask(__name__, template_folder="./business_layer/templates")
app.config["SECRET_KEY"] = generate_secret_key(31) # 31 chars, ~ 128-bit key
app.config["SESSION_TYPE"] = "filesystem"
# csrf
csrf = CSRFProtect(app)
# jinja filter/s
#app.jinja_env.filters['json_dumps_filter'] = json_dumps_filter
# rest of app configs
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_FILE_DIR"] = gettempdir()
Session(app)

#-----------------------General pages-----------------------
@app.route("/")
def default_page():
    return redirect(url_for("home_page"))

@app.route("/home")
def home_page():
    return render_template("index.html", navbar=NAVBAR)

#-----------------------Login pages-----------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    return do_login()

@app.route("/logout")
def logout():
    return do_logout()

@app.route("/register", methods=["GET", "POST"])
def register():
    return do_register()

#-----------------------Student pages-----------------------
@student_login_required
@app.route("/student/home")
def student_classes_view():
    return do_student_home_page()

@student_login_required
@app.route("/student/payments")
def student_payments():
    return do_payments()

#-----------------------Teacher pages-----------------------
@app.route("/teacher/home")
def teacher_classes_view():
    '''TODO'''

    pass
   
#-----------------------API pages-----------------------
@app.route("/api/student_calendar/", defaults={'schedule_id': -1})
@app.route("/api/student_calendar/<schedule_id>")    
def get_calendar(schedule_id):
    return do_get_calendar(schedule_id)

@app.route("/api/student_calendar/<schedule_id>/<month_id>")
def get_calendar_via_month(schedule_id, month_id):
    return do_get_calendar(schedule_id, month_id=month_id)

@app.route("/api/error", methods=["POST"])
def error_():
    return do_error()

@app.route("/api/payments")
def get_payments():
    return do_get_payments()


#-----------------------Launch the app-----------------------
if __name__ == "__main__":
    app.run()