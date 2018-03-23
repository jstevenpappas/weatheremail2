"""
.. module:: init
   :synopsis: Module factory method create_app() that initializes our Flask
        application.
.. moduleauthor:: John Pappas <jstevenpappas at gmail.com>

"""

import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_caching import Cache
from flask_mail import Mail
from flask_recaptcha import ReCaptcha

from .models import db, Person, City

from instance.config import env_config

app = Flask(__name__, instance_relative_config=True)
mail = Mail()
cache = Cache()
recaptcha = ReCaptcha()


def create_app(config_envar=None,
               env='default'):
    """Factory method returning a configured app context


    Notes:
          If config_en variable is None and there isn't an external config file
            passed in, then the the value in the 'env' arg is
            used.

     Args:
         config_envar (str): Env var pointing to file that has key=value pairs
            necessary for application to run.
         env (str): dict key used to return a config class from instance.config
            Flask app to run.
                Defaults to 'default'.

     Attributes:
         app: contains Flask app and context - nothing happens without this
         mail: provides access to and configuration for Flask_Mail
         cache: provides access to and configuration for Flask_Cache
         db: access and entry point for Flask_SqlAlchemy
         recaptcha: access to and configuration for Flask_Recaptcha
     """
    app.config.from_object(env_config[env])
    if config_envar:
        app.config.from_envvar(config_envar)
    mail.init_app(app)
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})
    db.app = app
    db.init_app(app)
    db.create_all()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = RotatingFileHandler('{name}.log'.format(name=__name__),
                                  maxBytes=100000, backupCount=3)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    recaptcha.init_app(app)
    return app


"""
These imports are here intentionally.
They need to be imported after the Flask app is instantiated via create_app() 
    but not beforehand b/c they will fail otherwise.  
This would seem to be a circular dependency but __init__.py doesn't depend on 
    views or commands so it poses little to no risk.
"""
import weatheremail2.views
import weatheremail2.commands
