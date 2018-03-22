"""
.. module:: utils
   :synopsis: Module containing helper methods.
.. moduleauthor:: John Pappas <jstevenpappas at gmail.com>

"""
import csv
import os

import jsonpickle

from .app_error import AppError


def encode_to_json_for_session(var):
    """Returns jsonpickle encoded strings for store in Flask session.

    Notes:
        There are better explanations online than this but in short: values
            written to the session by app code will be put in a
            cryptographically signed cookie sent to the client.
        Because it is going from the server to the client over the network,
            it needs to be serialized.

    Args:
        var (str): Any value we want to store in session.

    Returns:
        encoded string that is able to be stored in session

    """
    return jsonpickle.encode(var)


def get_data_file(subdir='data', filename=None):
    """Returns absolute path of file containing city,state data.

    Args:
        api_key (str): Wunderground Weather API Key.
        data (dict): values described above

    Returns:
        populated URI str for which to access weather data API

    Raises:
        TypeError wrapped with AppError: If positional params subdir or
            filename are passed with invalid data.

    """
    try:
        if subdir is None:
            root_dir = os.path.dirname(os.path.abspath(__file__))
            abs_path = os.path.join(root_dir, filename)
            return abs_path
        else:
            root_dir = os.path.dirname(os.path.abspath(__file__))
            file_dir = os.path.join(root_dir, subdir)
            abs_path = os.path.join(file_dir, filename)
            return abs_path
    except TypeError as te:
        raise AppError('Unable to build absolute path for file containing city data.', te)


def get_city_data(loadfile='top_100_city_state_sorted.txt'):
    """Returns city,state data from text file in data directory.

    Args:
        loadfile (str): Filename containing city, state data.

    Returns:
        Generator of list objects

    Raises:
        FileNotFoundError wrapped with AppError: If file not able to be found

    """
    try:
        cities_file = get_data_file(filename=loadfile)
        with open(cities_file) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                yield row
    except FileNotFoundError as fnfe:
        raise AppError('Unable to find file to load city data from.', fnfe)


def get_username_from_email(email_address):
    """Returns username portion of email.

    Args:
        email_address (str): email address of person model

    Returns:
        username portion of email address

    Raises:
        AttributeError wrapped with AppError: If None passed as param

    """
    try:

        username_portion = email_address.split("@")[0]
        return username_portion
    except AttributeError as ae:
        raise AppError('Unable to parse username from email address.', ae)
