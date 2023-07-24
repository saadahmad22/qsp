'''This is the main module of forms, which handles html forms

This module stores conviencince classes to be used in the app. 
These classes are implemented with wtforms to get secure information to and from user. 

Usage:
    You can use this module as follows:

    >>> from data.forms import ExampleForm
    >>> ...
    >>> build the flask app
    >>> ...
    >>> @app.route(route_address)
    >>> def route_method():
    >>>     form = ExampleForm()
    >>>     form.update()
    >>>     if request.method == 'POST' and form.validate():
    >>>         ...
    >>>         return the relevant route after dealing with the inputs as wanted
    >>>     return the relavnt page and pass in the form, like so: render_template("page.html", form=form)

Classes:
    RegisterForm: A class to serve base contruct for the registeration screen form 

'''

from .register_form import RegisterForm
from .login_form import LoginForm

__all__ = ["RegisterForm", "LoginForm"]