from flask import url_for
from flask.ext import testing
from tests.base import base
from steerclear import app, db
from steerclear.models import User

import phonenumbers

# name of templates used by the login module
LOGIN_TEMPLATE_NAME = 'login.html'
REGISTER_TEMPLATE_NAME = 'login.html'

"""
SteerClearLoginTestCase
-----------------------
TestCase for testing the login module
"""
class SteerClearLoginTestCase(base.SteerClearBaseTestCase):

    """
    setUp
    -----
    called before each test function. creates new test database
    """
    def setUp(self):
        super(SteerClearLoginTestCase, self).setUp()
        self.payload = {
            u'email': u'ryan',
            u'password': u'1234',
            u'phone': '+12223334444'
        }

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
    test_login_failure_incorrect_email
    -------------------------------------
    Tests that login fails if the user supplies the wrong email
    """
    def test_login_failure_incorrect_email(self):
        # test with no Users in db
        response = self.client.post(url_for('login.login'), data=self.payload)
        self.assertTemplateUsed(LOGIN_TEMPLATE_NAME)
        self.assertTrue(response.status_code, 200)

        # test with user that has different email but same password
        self._create_user(email='kyle', password='1234')
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

        # test with user that has same email but different password
        self._create_user(email='ryan', password='4321')
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
        self._create_user(email='ryan', password='1234')
        response = self.client.post(url_for('login.login'), data=self.payload)
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
        self._create_user(email='ryan', password='1234')
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
    test_register_failure_email_exists
    -------------------------------------
    Tests that trying to register a new user with
    a email that already exists fails
    """
    def test_register_failure_email_exists(self):
        # create a user
        self._create_user(email='ryan', password='1234')

        # check that POST request failed
        response = self.client.post(url_for('login.register'), data=self.payload)
        self.assertEquals(response.status_code, 409)
        self.assertTemplateUsed(REGISTER_TEMPLATE_NAME)
        self.assertContext('action', url_for('login.register'))

    """
    test_register_success
    ---------------------
    Tests that we can register a new user successfully
    """
    def test_register_success(self):
        # create user and check for success in response
        response = self.client.post(url_for('login.register'), data=self.payload)
        self.assertRedirects(response, url_for('login.login'))

        # find new user in db and check that it has correct email/password
        user = User.query.filter_by(email=self.payload[u'email']).first()
        self.assertIsNotNone(user)
        self.assertEquals(user.email, self.payload[u'email'])
        self.assertEquals(user.password, self.payload[u'password'])
        self.assertEquals(user.phone.e164, self.payload[u'phone'])

        # make sure we can log in as new user
        response = self.client.post(url_for('login.login'), data=self.payload)
        self.assertRedirects(response, url_for('driver_portal.index'))
