from flask import url_for
from flask.ext import testing
from steerclear import app, db
from steerclear.models import User, Ride

from datetime import datetime

"""
SteerClearLoginTestCase
-----------------------
TestCase for testing the login module
"""
class SteerClearBaseTestCase(testing.TestCase):

    # do not render templates in responses
    render_templates = False

    """
    create_app
    ----------
    Creates an instance of the steerclear flask app
    and sets up testing context
    """
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['TEST_SQLALCHEMY_DATABASE_URI']
        return app

    """
    setUp
    -----
    called before each test function. creates new test database
    """
    def setUp(self):
        db.create_all()

    """
    tearDown
    --------
    called after each test function. breaks down test fixtures
    """
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    """
    _login
    ------
    Helper function that creates a user and then logins as that user
    """
    def _login(self):
        user = User(email='ryan', password='1234')
        db.session.add(user)
        db.session.commit()
        self.client.post(url_for('login.login'), data={
                u'email': u'ryan',
                u'password': u'1234'
            })

    """
    _logout
    -------
    Helper function that logs the current user out
    """
    def _logout(self):
        return self.client.get(url_for('login.logout'))

    """
    _create_user
    ------------
    Helper function that creates and returns a new User object in the db
    """
    def _create_user(self, email='ryan', password='1234'):
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    """
    _create_ride
    ------------
    Helper function that creates and returns a new Ride object in the db
    """
    def _create_ride(self, num_passengers=0, start_latitude=1.0, start_longitude=1.1, end_latitude=2.0, end_longitude=2.1, pickup_time=datetime(1,1,1), travel_time=datetime(1,1,1), dropoff_time=datetime(1,1,1)):
        ride = Ride(
            num_passengers=num_passengers,
            start_latitude=start_latitude,
            start_longitude=start_longitude,
            end_latitude=end_latitude,
            end_longitude=end_longitude
        )
        db.session.add(user)
        db.session.commit()
        return user
