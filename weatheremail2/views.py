"""
.. module:: views
   :synopsis: Module containing routes for Flask application.
.. moduleauthor:: John Pappas <jstevenpappas at gmail.com>

"""

from flask import request, redirect, render_template, url_for, flash, session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import BadRequest

from weatheremail2 import app, cache, recaptcha
from .app_error import AppError
from .forms import ContactForm
from .models import db, Person, City
from .utils import encode_to_json_for_session


@app.route('/', methods=['GET', 'POST'])
def signup():
    """Route for application main page.

    Notes:
        GET request:
            Returns page with form allowing user to enter email and
            select from drop down list a city from which to receive
            weather status updates.
        POST request:
            Communicates errors via flash messages.
            For a form submission to be successful, the following must be
                true:
                1) email element is not empty
                2) the Google Recaptcha was satisfied
                3) form is validated
                4) the email is not a duplicate of a previous submission
            If these items are satisfied, then:
                1) the city id is used to reify a City model from the
                    database so we can confirm it exists on our side and is
                    not malicious input
                2) a Person is created using the email and city_id
                    and persisted to the database
                3) the city/state/email is put in the users session and
                    via a Post/Redirect/Get, the user is presented with
                    a success page

    Raises:
         SQLAlchemyError, AppError, BadRequest
    """
    form = ContactForm()
    try:
        if request.method == 'POST':
            if not (form.email.data and recaptcha.verify()):
                flash(
                    "Please provide an email address and solve the captcha "
                    "so we can send you your weather!",
                    category='error')

            else:

                if form.validate_on_submit():
                    email = form.email.data
                    person_exists = Person.query.filter_by(email=email).first()

                    if person_exists:
                        flash(
                            "We have your email - please check your inbox or "
                            "provide another address!",
                            category='info')
                    else:

                        city = request.form.get('location')

                        selected_city = City.query.filter_by(
                            id=int(city)).first()

                        person = Person(email=email, city_id=selected_city.id)
                        db.session.add(person)
                        db.session.commit()
                        session['city'] = encode_to_json_for_session(
                            selected_city.name)
                        session['state'] = encode_to_json_for_session(
                            selected_city.state)
                        session['email'] = encode_to_json_for_session(
                            person.email)

                        flash("thank you for signing up for weather alerts",
                              category='success')

                        return redirect(url_for('.success'), code=303)
                else:
                    flash(
                        "We could not validate your form submission - please "
                        "try again!",
                        category='error')

        cached_cities = get_all_cities()
        return render_template('signup.html', title='weather email signup',
                               form=form, cities=cached_cities)
    except (SQLAlchemyError, AppError, BadRequest) as gen_exc:
        app.logger.error(
            'We got the following exception during in email signup page: %s',
            gen_exc)


@cache.cached(timeout=600, key_prefix='all_cities')
def get_all_cities():
    """Method returns cities for drop-down select on signup page.

    Notes:
        This is cached w/ a 10 min expiry so application not incur overhead of
            data access for every page load.
        City data returned by method is great candidate for caching since it
            will rarely become change.

    Raises:
         AppError: If no city results returned from database.
    """
    try:
        cities = City.query.order_by('name').all()
        return cities
    except NoResultFound as nrf_exc:
        raise AppError(
            'No city data was returned from the database for which to '
            'populate the signup page drop down.',
            nrf_exc)


@app.route('/success', methods=['GET'])
def success():
    """Route for confirmation page.

    Notes:
        Retrieves city/state/email data from session as opposed to request
            params so we can be sure that only data associated with user is
            displayed.

    Raises:
        ValueError, KeyError: If req'd info not accessible from session or
            session stored info not json encoded
    """
    try:
        email = session['email']
        city = session['city']
        state = session['state']
        return render_template('success.html', email=email, city=city,
                               state=state)
    except (ValueError, KeyError) as missing_session_data_ex:
        app.logger.warning(
            'Missing Session Data: Request to /success was missing one more '
            'datum in their session: %s  %s',
            type(missing_session_data_ex.args), missing_session_data_ex)
        session.pop('_flashes', None)
        return render_template('error_bookmarked_url.html')


@app.errorhandler(404)
def page_not_found(err_404):
    """Error handler for HTTP Status code 404 errors"""
    app.logger.warning('404 page generated for user: %s', err_404)
    session.pop('_flashes', None)
    return render_template('error_http_404.html'), 404


@app.errorhandler(500)
def server_not_available(err_500):
    """Error handler for HTTP Status code 500 errors"""
    app.logger.error('500 page generated for user: %s', err_500)
    session.pop('_flashes', None)
    return render_template('error_http_500.html'), 500
