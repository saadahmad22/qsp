import sys
from functools import wraps

from flask import flash, redirect, render_template, request, session, url_for
from passlib.apps import custom_app_context as pwd_context

# append the path of the parent directory
sys.path.append("..")

from data_access.db import (DataBaseHandler, LogicalOperator, Operation,
                            RelationalOperator)
from data_access.models import User

from .forms import LoginForm, RegisterForm

db_handler = DataBaseHandler()


def student_login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        elif int(session.get("permission_level")) >= 1:
        # CHANGE: elif str(session.get("role")) == "student":
            return redirect(url_for("teacher_classes_view"), next = request.url)
        return f(*args, **kwargs)
    return decorated_function

def teacher_login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        elif int(session.get("permission_level")) == 0:
        # CHANGE: elif str(session.get("role")) == "admin":
            return redirect(url_for("teacher_classes_view"), next = request.url)
        return f(*args, **kwargs)
    return decorated_function

def do_logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

def do_login():
    """Log user in."""

    # forget any user_id
    session.clear()

    form = LoginForm(request.form)
    login_page = "login.html"

    # if user reached route via POST (as by submitting a form via POST)
    if form.validate_on_submit():
        # query database for username
        try :
            current_user = read_login_form(form)
        except Exception as error:
            print(error)
            current_user = None

        issue_present = False
        # ensure username exists and password is correct
        if current_user is None:
            flash("This email could not be found.", "danger")
            issue_present = True
        elif not pwd_context.verify(str(form.password.data), current_user.__vars__["password_hash"]):
            flash("This password is incorrect", "danger")
            issue_present = True
            
        if issue_present == True:
            return render_template(login_page, form=form)

        # remember which user has logged in
        session["user_id"] = current_user.__vars__["user_id"]
        session["permission_level"] = current_user.__vars__["role"]

        # redirect user to home page
        return redirect(url_for("default_page"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template(login_page, form=form)
    
def read_login_form(form : LoginForm) -> User:
    '''Returns a list of Users (fetched from the db) from the data retrieved in login_form'''

    search_args = Operation("users.email", f'{str(form.email.data)}', RelationalOperator.EQ)
    return db_handler.fetch(User(), "users", [search_args], [])

def do_register():
    """Register user."""
    # POST receives, while the other sends. Validation will occur by JS as much as possible, and the rest will offload here
    # implemented using wtf forms to have secure password coming over
    form = RegisterForm(request.form)
    register_page = "register.html"

    # if user reached route via POST (as by submitting a form via POST)
    if form.validate_on_submit():
        needs_to_redo_form = False

        # ensure email is unique
        rows = db.execute("SELECT * FROM users WHERE email = ?", (str(form.data["email"]),))
        # CHANGE: rows = db.execute("SELECT * FROM users WHERE email = ?", (str(form.data["email"]),))
        if len(rows) >= 1:
            flash("The email you selected is already in use. Please select another username", "danger")
            needs_to_redo_form = True

        # this makes all the error messages and then sends the user back
        if needs_to_redo_form == True:
            return render_template(register_page, form=form)

        # add user to database
        db.execute("INSERT INTO users (first, last, password_hash, email, time_stamp, permission_levels) VALUES (?, ?, ?, ?, ?, ?)",
            (
            str(form.data["first_name"]), 
            str(form.data["last_name"]),
            str(pwd_context.encrypt(form.password.data)),
            str(form.data["email"]),
            format_for_sql(convert_time(current_time())),
            0
            )
        )
        # CHANGE TO (NOTE: add phone number field to the form control)
        # db.execute("INSERT INTO users (first, last, password_hash, email, phone, role) VALUES (?, ?, ?, ?, ?, ?)",
        #     (
        #     str(form.data["first_name"]), 
        #     str(form.data["last_name"]),
        #     str(pwd_context.encrypt(form.password.data)),
        #     str(form.data["email"]),
        #     str(form.data["phone"]),
        #     'student'
        #     )
        # )

        # login user automatically and remember session
        rows = db.execute("SELECT user_id FROM users WHERE email == ?", (str(form.data["email"]),))
        session["user_id"] = rows[0][0]
        session["permission_level"] = 0
        # CHANGE: session["role"] = rows[0][2]

        # redirect to home page
        return redirect(url_for("student_classes_view"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        for field, errors in form.errors.items():
            if (field == "first_name") or (field == "last_name"):
                flash("Please enter you name in the First and Last name boxes", "danger")
            elif (field == "email"):
                flash("Please enter a valid, unused email address in the Email input box", "danger")
            elif (field == "password"):
                flash("Please enter a valid password in the Password input box.",
                       "danger")
                form.password.errors = ['Please enter a password which has a lowercase and uppercase letter, a number, a special character, and is 6-20 characters long']
            elif (field == "confirm_password"):
                flash('The "Confirmed Password" input box must match the "Password" input box', "danger")
            else:
                flash("An unkown error has occurred", "danger")

        
        return render_template(register_page, form=form)