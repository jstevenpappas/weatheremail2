"""
.. module:: forms
   :synopsis: Module containing FlaskForm used in our app.
.. moduleauthor:: John Pappas <jstevenpappas at gmail.com>

"""
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email


class ContactForm(FlaskForm):
    """Form class customized for our signup page

    Attributes:
        email (EmailField): class containing validators specific to emails.
        submit (SubmitField): class integrating submit functionality with Form.
    """
    email = EmailField("Email", validators=[
        InputRequired("Please enter your email address."),
        Email("Please enter your email address.")])
    submit = SubmitField("Submit Email")
