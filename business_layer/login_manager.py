import sys
from functools import wraps

from flask import flash, redirect, render_template, request, session, url_for
from passlib.apps import custom_app_context as pwd_context

# append the path of the parent directory
sys.path.append("..")

from configs import NAVBAR

from data_access.db import DataBaseHandler, fetch_user
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
        elif str(session.get("role")) == "teacher":
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
        elif str(session.get("role")) == "student":
            return redirect(url_for("student_classes_view"), next = request.url)
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
            current_user = fetch_user(email=str(form.email.data))
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
            return render_template(login_page, form=form, navbar=NAVBAR)

        # remember which user has logged in
        session["user_id"] = current_user.__vars__["user_id"]
        session["role"] = current_user.__vars__["role"]

        # redirect user to home page
        return redirect(url_for("student_classes_view"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template(login_page, form=form, navbar=NAVBAR)

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
        try :
            current_user = fetch_user(email=str(form.email.data))
        except Exception as error:
            print(error)
            current_user = None

        if current_user is not None:
            flash("The email you selected is already in use. Please select another email", "danger")
            print(current_user)
            needs_to_redo_form = True

        # this makes all the error messages and then sends the user back
        if needs_to_redo_form:
            return render_template(register_page, form=form, navbar=NAVBAR)

        # add user to database
        new_user = User()
        data = (form.first_name.data, form.last_name.data, form.email.data, form.phone.data, 
                pwd_context.hash(form.password.data), '"student"')
        keys = tuple(new_user.__vars__.keys()) # to only fetch once and save iteration time
        for i, val in enumerate(data):
            new_user.__vars__[keys[1 + i]] = data[i]
        db_handler.save("users", new_user)

        
        session["user_id"] = fetch_user(form).__vars__["user_id"]
        session["role"] = "student"

        # redirect to home page
        return redirect(url_for("student_classes_view"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        for field, errors in form.errors.items():
            if (field == "first_name") or (field == "last_name"):
                flash("Please enter you name in the First and Last name boxes", "danger")
            elif (field == "email"):
                flash("Please enter a valid, unused email address in the Email box", "danger")
            elif (field == "password"):
                flash("Please enter a valid password in the Password box.", "danger")
                form.password.errors = ['Please enter a password which has a lowercase and uppercase letter, a number, a special character, and is 6-20 characters long']
            elif (field == "confirm_password"):
                flash('The "Confirmed Password" box must match the "Password" box', "danger")
            elif (field == "phone"):
                flash("Please enter a valid phone number in the Phone Number box.", "danger")
            else:
                flash("An unknown error has occurred", "danger")

        
        return render_template(register_page, form=form, navbar=NAVBAR)