from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Regexp, Email

class LoginForm(FlaskForm):
    '''A class to serve base construct for login forms 

    This class represents a username, email, and submit button. Other fields can be added as needed
      using different objects from the wtforms module.
    
    Attributes:
        username (StringField): makes a username field with the requirements of needing data 
            and being unique
        password (PasswordField): makes a password field with the requirements of needing data, 
            being a certain length, and meeting the regex requirements. in addition, 
            it securely stores and transmits the password from the user to the server.
            regex requirements:
                - 1+ lower case
                - 1+ upper case
                - 1+ digit
                - 1+ special character from @$!%*?& 
                - 6-20 characters minimum from the above categories

    Methods:
        None

    '''
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder" : "Email" })

    password = PasswordField(
        'Password', 
        validators=
        [
            DataRequired(),
            Regexp(regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=\[\]{};:"|\\<>,./?]).{6,20}$')
        ], 
        render_kw={"placeholder" : "Password" }
    )

    submit = SubmitField("Login")

