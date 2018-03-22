"""
.. module:: tests
   :synopsis: Unit tests for the  weatheremail application.
.. moduleauthor:: John Pappas <jstevenpappas at gmail.com>

"""

import time
import unittest

import mock

from weatheremail2 import create_app, db, mail
from weatheremail2.emails import send_weather_email, get_email_subject
from weatheremail2.models import City, Person
from weatheremail2.utils import get_username_from_email
from weatheremail2.wunderground import Forecast


class WeatherEmailTestCase(unittest.TestCase):
    """WeatherEmailTestCase tests the core functionality
    of the application.

	    Note:
	        Email tests in test_send_weather_email() contains a
	        time.sleep() to account for the time it takes emails to
	        be sent in the background and end up in the testing
	        'outbox' so they can be evaluated.
	        If the sleep weren't there, the test would run till finish
	        while the emails were still processing and any assertions
	        would fail.

    """
    def setUp(self):
        self.app = create_app(default_config='weatheremail2.config.TestingConfig')
        self.mail = mail
        self.client = self.app.test_client
        with self.app.app_context():
            db.create_all()
            boston = City(name='Boston', state='MA')
            houston = City(name='Houston', state='TX')
            db.session.add(boston)
            db.session.add(houston)
            db.session.commit()

            boston = City.query.filter_by(name='Boston').first()
            person = Person(email='someguy@whatevs.com', city_id=boston.id)
            db.session.add(person)
            db.session.commit()

    def test_main_page(self):
        """Test index page for sanity"""
        response = self.client().get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_cities_in_drop_down(self):
        """Test cities present in select drop down"""
        response = self.client().get('/', follow_redirects=True)
        self.assertIn(b'Boston, MA', response.data)
        self.assertIn(b'Houston, TX', response.data)

    def test_valid_email_signup(self):
        """Test valid email and city signup"""
        test_email = 'hello111@domain.com'
        city = City.query.filter_by(name='Boston').first()
        response = self.client().post('/', data={'email': test_email,
                                                 'location': city.id
                                                }, follow_redirects=True)
        self.assertIn(b'Congratulations', response.data)

    def test_unique_email_signup(self):
        """Test flash warning of preexisting email submission"""
        test_email = 'someguy@whatevs.com'
        city = City.query.filter_by(name='Boston').first()
        response = self.client().post('/', data={'email': test_email,
                                                 'location': city.id
                                                }, follow_redirects=True)
        self.assertIn(b'We have your email', response.data)



    def test_get_username_from_email(self):
        """Test splitting off username out of email address to get a pseudo-username"""
        email_addr = 'john_whatevs@email.com'
        expected = 'john_whatevs'
        actual = get_username_from_email(email_addr)
        self.assertEqual(expected, actual)

    def test_get_email_subject(self):
        """Test getting correct subject line based on weather conditions"""
        expected = "Not so nice out? That's okay, enjoy a discount on us."
        conditions = 'sleet'
        actual = get_email_subject(conditions)
        self.assertEqual(expected, actual)


    @mock.patch('weatheremail2.wunderground.requests.get')
    def test_get_weather_from_api(self, mock_get):
        """Test getting back correct (temp, conditions) tuple from weather api
		call and subsequent JSON parsing"""
        api_key = self.app.config['API_KEY_WUNDERGROUND']
        state = 'AL'
        city = 'Birmingham'
        mock_response = mock.Mock()
        mock_get.return_value = mock_response
        mock_response.text = '{ "current_observation": { "temp_f": 51.2, "icon": "cloudy" } }'
        expected_temperature = 51.2
        expected_conditions = 'cloudy'
        mock_forecast = Forecast.forecast_factory(api_key, state, city)
        self.assertEqual(expected_temperature, mock_forecast.temperature)
        self.assertEqual(expected_conditions, mock_forecast.conditions)


    def test_send_weather_email(self):
        """Test that we can send emails and get expected content"""
        sender = self.app.config['MAIL_USERNAME']
        email_address = 'hello111@domain.com'
        username = 'hello111'
        conditions = 'cloudy'
        city = 'Birmingham'
        state = 'AL'
        temp = 51.2
        expected_body = '<p>Hi hello111,</p>\n\n<p>The conditions for Birmingham,' \
						' AL are cloudy and the temperature is ' \
                        '' \
                        '' \
                        '' \
                        '51.2 F.</p>\n<p>Sincerely,</p>\n<p>The Weather Email team</p>'
        with self.app.app_context():
            with self.mail.record_messages() as outbox:
                send_weather_email(sender, email_address, username, conditions, city, state, temp)
                # not optimal but since sending async in thread, the above func will return
                # before finished unless we put in a time delay
                time.sleep(10)
                self.assertEqual(1, len(outbox))
                self.assertEqual(expected_body, outbox[0].html)

    def test_custom_handler_404(self):
        """Test 404 handler"""
        path = '/non_existent_endpoint'
        response = self.client().get(path)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page Not Found', response.data)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
