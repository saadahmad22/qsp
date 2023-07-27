from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired, Regexp, Email

class StdHomePage(FlaskForm):
    selected_class = SelectField("Select Class", coerce=int)

    submit = SubmitField("Go")