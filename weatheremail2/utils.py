"""
.. module:: utils
   :platform: Unix, Windows
   :synopsis: Module containing helper methods.
.. moduleauthor:: John Pappas <jstevenpappas at gmail.com>

"""
import csv
import os

import jsonpickle

from .app_error import AppError


def encode_to_json_for_session(var):
    """

    :param var:
    :return:
    """
    return jsonpickle.encode(var)


def get_data_file(subdir='data', filename=None):
    """

    :param subdir:
    :param filename:
    :return:
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
    """

    :param loadfile:
    :return:
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
    """

    :param email_address:
    :return:
    """
    try:

        username_portion = email_address.split("@")[0]
        return username_portion
    except AttributeError as ae:
        raise AppError('Unable to parse username from email address.', ae)
