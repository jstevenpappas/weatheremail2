"""
.. module:: emails
   :synopsis: Email module to provide convenience methods for sending emails.
.. moduleauthor:: John Pappas <jstevenpappas at gmail.com>

"""

from flask import render_template
from flask_mail import Message

from weatheremail2 import mail, app
from .decorators import async_in_thread

FORECAST_CONDITIONS_MAP = {
    'sunny': "It's nice out! Enjoy a discount on us.",
    'clear': "It's nice out! Enjoy a discount on us.",
    'chanceflurries': "Enjoy a discount on us.",
    'chancerain': "Enjoy a discount on us.",
    'chancesleet': "Enjoy a discount on us.",
    'chancesnow': "Enjoy a discount on us.",
    'chancetstorms': "Enjoy a discount on us.",
    'partlycloudy': "Enjoy a discount on us.",
    'mostlycloudy': "Enjoy a discount on us.",
    'mostlysunny': "Enjoy a discount on us.",
    'partlysunny': "Enjoy a discount on us.",
    'rain': "Not so nice out? That's okay, enjoy a discount on us.",
    'sleet': "Not so nice out? That's okay, enjoy a discount on us.",
    'snow': "Not so nice out? That's okay, enjoy a discount on us.",
    'flurries': "Not so nice out? That's okay, enjoy a discount on us.",
    'fog': "Not so nice out? That's okay, enjoy a discount on us.",
    'hazy': "Not so nice out? That's okay, enjoy a discount on us.",
    'tstorms': "Not so nice out? That's okay, enjoy a discount on us.",
    'cloudy': "Not so nice out? That's okay, enjoy a discount on us."
}


@async_in_thread
def send_email(subject, sender, recipients, html_body):
    """Method that peforms actual sending of email.

    Notes:
        Annotated with @async_in_thread meaning that each email send
            will run in its own thread until completion
    """
    with app.app_context():
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.html = html_body
        mail.send(msg)


def send_weather_email(sender, email, username, conditions, city, state, temp):
    """Method that prepares for sending emails by setting core values and
        populating template with city/state/temp/conditions data.

    Args:
         sender (str): email address of  account from which emails are sent
         email (str): recipients email
         username (str): portion of email before @.
         conditoins (str): string describing weather
         city (str): name of city
         state (str): 2 char state abbrev.
         temp : temperature in F

    Attributes:
        conditional_subject: the subject line of the emails that is
            dependent on the weather conditions.



     """
    conditional_subject = FORECAST_CONDITIONS_MAP.get(conditions)
    send_email(conditional_subject,
               sender=sender,
               recipients=[email],
               html_body=render_template('email/weather_update.html',
                                         username=username,
                                         conditions=conditions,
                                         city=city,
                                         state=state,
                                         temp=temp))


def get_email_subject(conditions):
    """Method that maps weather conditions with appropriate email subject"""
    try:
        return FORECAST_CONDITIONS_MAP.get(conditions)
    except KeyError as ke_exc:
        app.logger.error('Missing key for condition->email-subject mapping '
                         'for weather update emails: %s', ke_exc)
        return "Enjoy a discount on us."
