"""
.. module:: wunderground
   :synopsis: Module containing class for accessing Wunderground weather API.
.. moduleauthor:: John Pappas <jstevenpappas at gmail.com>

"""

import json

import requests
from requests.exceptions import RequestException

from .app_error import AppError


class Forecast(object):
    """Wraps Wunderground API access

    Intended to be instantiated via the forecast_factory()
    classmethod herein.

    Attributes:
        API_BASE_URI (str): base URI to access Wunderground
        API_URI (str): preformatted for which to later populate



    """
    API_BASE_URI = 'http://api.wunderground.com/api'
    API_URI = API_BASE_URI + '/{api_key}/{feature_path}/q/{state}/{city}.{' \
                             'response_format}'

    def __init__(self, api_key, feature_path='conditions',
                 response_format='json'):
        """constructor to set up extract defaults for Forecast class

        Args:
            api_key (str): Wunderground Weather API Key.
            feature_path (str): Specifies the type of data requested.
                Defaults to 'conditions'.
            response_format (str): Data format.
                Defaults to 'json'

        Attributes:
            api_key (str): Wunderground Weather API Key.
            feature_path (str): Specifies the type of data requested.
                Defaults to 'conditions'
            response_format (str): Data interchange format.
                Defaults to 'json'
            conditions (str): Description of weather conditions.
            temperature (str): Temperature in F,
        """
        self.api_key = api_key
        self.feature_path = feature_path
        self.response_format = response_format
        self.conditions = None
        self.temperature = None

    @classmethod
    def forecast_factory(cls, api_key, state, city):
        """Factory method to return instance of Forecast.

        Args:
            api_key (str): Wunderground Weather API Key.
            city (str): Name of city.
            state (str): 2 char abbrev. for US state

        Returns:
            Forecast instance

        Raises:
            AppError: If RequestException or wrapped KeyError occur

        """
        try:
            forecast = Forecast(api_key)
            forecast_dict = forecast.__dict__
            request_formatted_city = city.replace(" ", "_")
            forecast_dict.update(
                {'state': state, 'city': request_formatted_city})
            request_uri = ('{uri}'.format(
                uri=forecast.build_api_uri(forecast.API_URI, forecast_dict)))
            response = requests.get(request_uri).text
            response_json = json.loads(response)
            forecast.temperature = response_json["current_observation"][
                'temp_f']
            forecast.conditions = response_json["current_observation"]['icon']
            return forecast
        except (RequestException, AppError) as re_exc:
            raise AppError(
                'An error occurred while accessing weather forecast API data.',
                re_exc)

    @staticmethod
    def build_api_uri(api_uri, data):
        """Builds API URI using dict of values.

        Args:
            api_key (str): Wunderground Weather API Key.
            data (dict): values described above

        Returns:
            populated URI str for which to access weather data API

        Raises:
            AppError: If KeyError

        """
        try:
            return api_uri.format(**data)
        except KeyError as ke_exc:
            raise AppError(
                'An error occurred while building the weather API URI.',
                ke_exc)
