from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir

from business_layer.login_manager import do_login, do_logout, do_register

from os import urandom as generate_secret_key

from flask import Flask



# create and configure the app/jinja enviroment
app = Flask(__name__, template_folder="./business_layer/templates")
app.config["SECRET_KEY"] = generate_secret_key(31) # 31 chars, ~ 128-bit key
app.config["SESSION_TYPE"] = "filesystem"
# crsf
csrf = CSRFProtect(app)
# jinja filter/s
#app.jinja_env.filters['json_dumps_filter'] = json_dumps_filter
# rest of app configs
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_FILE_DIR"] = gettempdir()
Session(app)

@app.route("/")
def default_page():
    return redirect(url_for("home_page"))

@app.route("/home")
def home_page():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    return do_login()

@app.route("/logout")
def logout():
    return do_logout()

@app.route("/student/home")
def student_classes_view():
    '''TODO'''

    pass

@app.route("/teacher/home")
def teacher_classes_view():
    '''TODO'''

    pass

@app.route("/register", methods=["GET", "POST"])
def register():
    return do_register()
   
if __name__ == "__main__":
    app.run()