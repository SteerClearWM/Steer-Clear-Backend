from flask import url_for
from flask.ext import testing
from steerclear import app, db
from steerclear.models import User

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
        user = User(username='ryan', password='1234')
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
