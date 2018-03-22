
"""Entry point for the Flask application

The flask app is created via the create_app() factory
method.   If you don't pass in an APP_SETTINGS to the
environment, the config.DefaultConfig class will take precedence.

Example:
    2 env variables are helpful:
        1) export FLASK_APP=run.py
        2) export APP_SETTINGS=/path/to/settings.cfg


        $ flask run

    If you do neither of the above, you can still run the app
    using 'python run.py' provided you set the values in the
    config.DefaultConfig class

"""

from os import environ

from weatheremail2 import create_app

if environ.get('APP_SETTINGS'):
    app = create_app(config_envar='APP_SETTINGS')
else:
    # take config.DefaultConfig as default
    app = create_app()

if __name__ == "__main__":
    app.run(debug=False)  # note: this is setting debug=False
