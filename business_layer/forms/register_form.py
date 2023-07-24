from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email

from .login_form import LoginForm

class RegisterForm(LoginForm):
    '''A class to serve base contruct for the registeration screen form 

    This class represents different fields and values in a registerartion screen
      using different objects from the wtforms module.
    
    Attributes:
        email (StringField): makes an email field with the requirements of needing data, being unique, 
            and for it to be in an email form
        username (StringField): makes a username field with the requirements of needing data 
            and being unique
        password (PasswordField): makes a password field with the requirements of needing data, 
            being a ceratain length, and meeting the regex requirements. in addition, 
            it securely stores and transmits the password from the user to the server.
            regex requirements:
                - 1+ lower case
                - 1+ upper case
                - 1+ digit
                - 1+ special character from @$!%*?& 
                - 6-20 characters minimum from the above categories
        confirm_pasword (PasswordField): makes a password field with the requirements of needing data,
            and matching with the password field
        submit (SubmitField): makes a submit field with the text 'Register'

    Methods:
        None

    '''

    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder" : "Email" })

    confirm_password = PasswordField(
        'Confirm Password', 
        validators=
        [
        DataRequired(),
        EqualTo('password', message='Passwords must match')
        ],
        render_kw={"placeholder" : "Confirm Password" }
    )

    first_name = StringField("First Name", validators=[DataRequired()], render_kw={"placeholder" : "First Name" })
    last_name = StringField("Last Name", validators=[DataRequired()], render_kw={"placeholder" : "Last Name" })

    submit = SubmitField("Register")