# WeatherEmail Application

#### Table of Contents

1. [Description](#description)
2. [Setup](#setup)
3. [Configuration](#configuration)
4. [Populating Data](#populating-data)
5. [Testing](#testing)
6. [Running The App](#running-the-app)
7. [Sending Emails](#sending-emails)
8. [Database Schema](#database-schema)
9. [Logging](#logging)

## Description

This app allows users to choose a city from a drop down and submit their email address.
The idea is that they will receive an email with the weather of their chosen city at some later time.
The application consists of two main parts: 1) the web app; and, 2) a command line utility to send users emails with weather updates.


## Setup
These instructions assume you are using the following:
* virtualenv
* virtualenvwrapper
* postgres database
* Python 3 (this project used 3.6.1)

Additionally, it is assumed you are able to acquire the following:
* Wunderground API key
* Google Gmail account
* Google Recaptcha site and secret key


* create a target dir and cd to it
    * ```mkdir /your/workspace/weatheremail2```
    * ```cd /your/workspace/weatheremail2```
* clone the repo
    * ```git clone https://github.com/jstevenpappas/weatheremail2.git```
* create the virtualenv
    * ```mkvirtualenv -p python2.7 -a /your/workspace/weatheremail2``
* activate the virtualenv
    * ```workon weatheremail2```
* install the modules
    * ```pip install -r requirements.txt```
* create a dev and test database (assumes PostgreSQL)
    * ```createdb weatheremail2_dev```
    * ```createdb weatheremail2_test```
* signup for a Wunderground API key at the following url:
    * [Wunderground API](https://www.wunderground.com/weather/api/)




## Configuration

Configuration values used by the application reside in the config module.

Your dev config would use DefaultConfig while your unit tests would use TestingConfig.

The following config values are the main ones you will need to provide with values:

* MAIL_USERNAME
* MAIL_PASSWORD
* RECAPTCHA_SECRET_KEY
* RECAPTCHA_SITE_KEY
* API_KEY_WUNDERGROUND
* SECRET_KEY
* WTF_CSRF_SECRET_KEY
* SQLALCHEMY_DATABASE_URI

If you wish to disable Recaptcha in dev, then you can set the following to false and leave the other Recapcha configs empty:
``` RECAPTCHA_ENABLED = False```

An alternative to relying on the config module for configuration, you can create a ```settings.cfg``` file and  put your configuration in there.


## Populating Data

At the command line, run the following to populate your database with city data:
```$ flask load_data```

This will drop and recreate the schema as well as populate the ```city``` table with data.


## Testing

To run the unit tests, do the following at the command line:
```$ python tests.py```

## Running The App
Assuming you have done the above, you can set the following at the command line:

```
export APP_SETTINGS=/Users/jpappas/workspace_python/weatheremail2/settings.cfg
export FLASK_APP=run.py
```

## Sending Emails

At the command line, run the following to populate your database with city data:
```$ flask send_weather_emails```

## Database Schema

**person**

| Column     | Datatype | Default | Meaning |
| ---      | ---       | ---     | ---      |
|id | int4 | primary_key |  sequential # assigned each row (surrogate key)          |
|email | Varchar(254 | unique |  email of person signing up      |
|city_id | int4 | ForeignKey('city.id'), NOT NULL |  FK ref to id corresponding to city chosen during signup      |
|time_created | timestamp with TZ | NOT NULL |  ts record created    |
|time_updated | timestamp with TZ | DEFAULT NULL |  ts record updated     |


**city**

| Column     | Datatype | Default | Meaning |
| ---      | ---       | ---     | ---      |
|id | int4 | primary_key |  sequential # assigned each row (surrogate key)          |
|name | Varchar(120 | unique, NOT NULL |  name of city     |
|state | Varchar(2) | NOT NULL | 2 char abbreviation representing state w/in which city resides      |


### Logging

Logfile locations are the following:
* /Mailing/analytics/seed_pulse/gmail_seedpulse.log
* /Mailing/analytics/seed_pulse/hotmail_seedpulse.log
* /Mailing/analytics/seed_pulse/yahoo_seedpulse.log
* /Mailing/analytics/seed_pulse/aol_seedpulse.log
