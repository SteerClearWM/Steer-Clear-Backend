from flask import url_for
from flask.ext import testing
import unittest
from steerclear import app, db

LOGIN_TEMPLATE_NAME = 'login.html'

class SteerClearLoginTestCase(testing.TestCase):

    render_templates = False

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['TEST_SQLALCHEMY_DATABASE_URI']
        return app

    """
    setUp
    -----
    called before each test function. Sets up flask app test
    instance and creates new test database
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

    def test_get_login_page(self):
        self.client.get(url_for('login.login'))
        self.assert_template_used(LOGIN_TEMPLATE_NAME)
