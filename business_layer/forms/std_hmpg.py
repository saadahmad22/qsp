from flask_wtf import FlaskForm
from wtforms import SelectField

class StdHomePage(FlaskForm):
    selected_class = SelectField("Select Class", coerce=int)