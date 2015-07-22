from flask import url_for
from flask.ext import testing
import unittest
from steerclear import app, db
from steerclear.models import User

# name of templates used by the login module
LOGIN_TEMPLATE_NAME = 'login.html'
REGISTER_TEMPLATE_NAME = 'login.html'

"""
SteerClearLoginTestCase
-----------------------
TestCase for testing the login module
"""
class SteerClearLoginTestCase(testing.TestCase):

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
        self.payload = {
            u'username': u'ryan',
            u'password': u'1234',
        }
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
    test_get_login_page
    -------------------
    Tests that GET request to login route 
    returns the login page
    """
    def test_get_login_page(self):
        response = self.client.get(url_for('login.login'))
        self.assertTemplateUsed(LOGIN_TEMPLATE_NAME)
        self.assertTrue(response.status_code, 200)
        self.assertContext('action', url_for('login.login'))

    """
    test_login_failure_incorrect_username
    -------------------------------------
    Tests that login fails if the user supplies the wrong username
    """
    def test_login_failure_incorrect_username(self):
        # test with no Users in db
        response = self.client.post(url_for('login.login'), data=self.payload)
        self.assertTemplateUsed(LOGIN_TEMPLATE_NAME)
        self.assertTrue(response.status_code, 200)

        # test with user that has different username but same password
        user = User(username='kyle', password='1234')
        db.session.add(user)
        db.session.commit()
        response = self.client.post(url_for('login.login'), data=self.payload)
        self.assertTemplateUsed(LOGIN_TEMPLATE_NAME)
        self.assertTrue(response.status_code, 200)
        self.assertContext('action', url_for('login.login'))

    """
    test_login_failure_incorrect_password
    -------------------------------------
    Tests that login fails if the user supplies the wrong password
    """
    def test_login_failure_incorrect_password(self):
        # test with no Users in db
        response = self.client.post(url_for('login.login'), data=self.payload)
        self.assertTemplateUsed(LOGIN_TEMPLATE_NAME)
        self.assertTrue(response.status_code, 200)

        # test with user that has same username but different password
        user = User(username='ryan', password='4321')
        db.session.add(user)
        db.session.commit()
        response = self.client.post(url_for('login.login'), data=self.payload)
        self.assertTemplateUsed(LOGIN_TEMPLATE_NAME)
        self.assertTrue(response.status_code, 200)
        self.assertContext('action', url_for('login.login'))

    """
    test_login_success
    ------------------
    Tests that a user can login successfully
    """
    def test_login_success(self):
        user = User(username='ryan', password='1234')
        db.session.add(user)
        db.session.commit()
        response = self.client.post(
            url_for('login.login'), 
            data=self.payload
        )
        self.assertRedirects(response, url_for('driver_portal.index'))

    """
    test_logout_requires_login
    --------------------------
    Tests that the logout route requires the user to be loged in
    """
    def test_logout_requires_login(self):
        response = self.client.get(url_for('login.logout'))
        self.assertEquals(response.status_code, 401)

    """
    test_logout_success
    -------------------
    Tests that a user can successfully logout
    """
    def test_logout_success(self):
        # login a user
        user = User(username='ryan', password='1234')
        db.session.add(user)
        db.session.commit()
        self.client.post(url_for('login.login'), data=self.payload)

        # logout user
        response = self.client.get(url_for('login.logout'))
        self.assertRedirects(response, url_for('login.login'))

        # make sure we are actually loged out
        response = self.client.get(url_for('login.logout'))
        self.assertEquals(response.status_code, 401)

    """
    test_get_register_page
    ----------------------
    Tests that we can GET the register page correctly
    with the right context
    """
    def test_get_register_page(self):
        # check that GET request succeeded
        response = self.client.get(url_for('login.register'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(REGISTER_TEMPLATE_NAME)
        self.assertContext('action', url_for('login.register'))

    """
    test_register_failure_username_exists
    -------------------------------------
    Tests that trying to register a new user with
    a username that already exists fails
    """
    def test_register_failure_username_exists(self):
        # create a user
        user = User(username='ryan', password='1234')
        db.session.add(user)
        db.session.commit()

        # check that POST request failed
        response = self.client.post(url_for('login.register'), data=self.payload)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(REGISTER_TEMPLATE_NAME)
        self.assertContext('action', url_for('login.register'))

    def test_register_success(self):
        response = self.client.post(url_for('login.register'), data=self.payload)
        self.assertRedirects(response, url_for('login.login'))