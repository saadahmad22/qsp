from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Regexp

from .login_form import LoginForm


class RegisterForm(LoginForm):
    '''A class to serve base construct for the registration screen form 

    This class represents different fields and values in a registration screen
      using different objects from the wtforms module.
    
    Attributes:
        email (StringField): makes an email field with the requirements of needing data, being unique, 
            and for it to be in an email form
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
        confirm_password (PasswordField): makes a password field with the requirements of needing data,
            and matching with the password field
        submit (SubmitField): makes a submit field with the text 'Register'

    Methods:
        None

    '''

    # NOTE: email and password inherited from loginform

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
    phone = StringField(
        'Phone', render_kw={"placeholder" : "Phone Number" }, validators=[
            DataRequired(), 
            Regexp(regex=r'^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$')
            ])


    submit = SubmitField("Register")