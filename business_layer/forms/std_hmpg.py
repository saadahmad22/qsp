from flask_wtf import FlaskForm
from wtforms import SelectField

class StdHomePage(FlaskForm):
    selected_class = SelectField("Select a class", coerce=int)