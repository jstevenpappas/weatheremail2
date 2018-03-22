"""
.. module:: commands
   :synopsis: Module containing methods providing for command line access to
        sending weather emails and creating the database schema and
        city/state data.
.. moduleauthor:: John Pappas <jstevenpappas at gmail.com>

"""

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

from weatheremail2 import app, cache
from .app_error import AppError
from .emails import send_weather_email
from .models import db, City, Person
from .utils import get_city_data, get_username_from_email
from .wunderground import Forecast


@app.cli.command()
def load_data():
    """Convenience method to create schema and necessary city/state data for
    app.

    Raises:
	   SQLAlchemyError, AppError: If database error or file containing
	    city data was unable to be parsed/loaded

    """
    try:
        db.drop_all()
        db.create_all()
        for row in get_city_data():
            city = City(name=str(row[0]).strip(), state=str(row[1]).strip())
            db.session.add(city)
        db.session.commit()
    except (SQLAlchemyError, AppError) as load_data_exc:
        app.logger.error('An error occurred while loading initial performing '
                         'the load_data command: %s', load_data_exc)


@app.cli.command()
def send_weather_emails():
    """Method to loop through the Person table and send
        emails containing the conditions and temperature
        of their selected city and state.

    Notes:
        This is executed at the command line:
            $ flask send_weather_emails

    Raises:
       AppError, SQLAlchemyError: If API data or database data is unavailable.
    """
    try:
        api_key = app.config['API_KEY_WUNDERGROUND']
        sender = app.config['MAIL_USERNAME']
        for email_address, city, state in get_user_data():
            forecast = get_cached_forecast(api_key, state, city)
            temp = forecast.temperature
            cond = forecast.conditions
            username = get_username_from_email(email_address)
            send_weather_email(sender, email_address, username, cond, city,
                               state, temp)
    except (SQLAlchemyError, AppError) as weather_emails_exc:
        app.logger.error('An error occurred during the execution of the '
                         'send_weather_emails command: %s', weather_emails_exc)


@cache.memoize(timeout=1200)
def get_cached_forecast(api_key, state, city):
    """Method using 'caching' that wraps the factory method that returns
        the Forecast class containing the temp and conditions data.

    Notes:
        This is cached using the method arguments as cache keys so
            cached entries are specific to a city/state/api_key.
        This allows us to avoid duplicate API requests and reuse already
            requested data.
    """
    return Forecast.forecast_factory(api_key, state, city)


def get_user_data():
    """Generator method returning email addresses and associated city and
        state data.

    Returns:
       Generator

    Raises:
       AppError: If no results from database occurs

    """
    try:
        for person, city in db.session.query(Person, City). \
                filter(Person.city_id == City.id).all():
            yield person.email, city.name, city.state
    except NoResultFound as nrf:
        raise AppError(
            'No user data was returned from the database for which to send '
            'weather emails: %s',
            nrf)
