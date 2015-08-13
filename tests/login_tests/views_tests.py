from flask import url_for
from flask.ext import testing
from tests.base import base
from steerclear import app, db
from steerclear.models import User, Role
from testfixtures import Replacer

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
        self.register_payload = {
            u'username': u'ryan',
            u'password': u'1234',
            u'phone': '+17572214000'
        }

        self.login_payload = {
            u'username': u'ryan',
            u'password': u'1234',
        }

        self.student_role = Role.query.filter_by(name='student').first()

    """
    test_get_login_page
    -------------------
    Tests that GET request to login route 
    returns the login page
    """
    def test_get_login_page(self):
        response = self.client.get(url_for('login.login'))
        self.assertTemplateUsed(LOGIN_TEMPLATE_NAME)
        self.assertEquals(response.status_code, 200)
        self.assertContext('action', url_for('login.login'))

    """
    test_login_failure_incorrect_email
    -------------------------------------
    Tests that login fails if the user supplies the wrong email
    """
    def test_login_failure_incorrect_email(self):
        # test with no Users in db
        response = self.client.post(url_for('login.login'), data=self.login_payload)
        self.assertTemplateUsed(LOGIN_TEMPLATE_NAME)
        self.assertEquals(response.status_code, 400)

        # test with user that has different email but same password
        self._create_user(email='kyle')
        response = self.client.post(url_for('login.login'), data=self.login_payload)
        self.assertTemplateUsed(LOGIN_TEMPLATE_NAME)
        self.assertEquals(response.status_code, 400)
        self.assertContext('action', url_for('login.login'))

    """
    test_login_failure_incorrect_password
    -------------------------------------
    Tests that login fails if the user supplies the wrong password
    """
    def test_login_failure_incorrect_password(self):
        # test with no Users in db
        response = self.client.post(url_for('login.login'), data=self.login_payload)
        self.assertTemplateUsed(LOGIN_TEMPLATE_NAME)
        self.assertEquals(response.status_code, 400)

        # test with user that has same email but different password
        self._create_user(email='ryan')
        response = self.client.post(url_for('login.login'), data=self.login_payload)
        self.assertTemplateUsed(LOGIN_TEMPLATE_NAME)
        self.assertEquals(response.status_code, 400)
        self.assertContext('action', url_for('login.login'))

    """
    test_login_failure_valid_credentials_but_hasnt_registered
    ---------------------------------------------------------
    Tests that a user who hasn't registered yet but
    attempts to login with valid W&M account credentials
    will fail to login
    """
    def test_login_failure_valid_credentials_but_hasnt_registered(self):
        # replace validate_user function so it passes
        with Replacer() as r:
            r.replace('steerclear.utils.cas.validate_user', self.mock_validate_user)

            # try to login
            response = self.client.post(url_for('login.login'), data=self.login_payload)
            self.assertTemplateUsed(LOGIN_TEMPLATE_NAME)
            self.assertEquals(response.status_code, 400)
            self.assertContext('action', url_for('login.login'))

    """
    test_login_success
    ------------------
    Tests that a user can login successfully
    """
    def test_login_success(self):
        # replace validate_user function so it passes
        with Replacer() as r:
            r.replace('steerclear.utils.cas.validate_user', self.mock_validate_user)
            self._create_user(email='ryan')
            response = self.client.post(url_for('login.login'), data=self.login_payload)
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
        # replace validate_user function so it passes
        with Replacer() as r:
            r.replace('steerclear.utils.cas.validate_user', self.mock_validate_user)
            
            # login a user
            self._create_user(email='ryan')
            self.client.post(url_for('login.login'), data=self.login_payload)

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
        # replace validate_user function so it passes
        with Replacer() as r:
            r.replace('steerclear.utils.cas.validate_user', self.mock_validate_user)
            # create a user
            self._create_user(email='ryan')

            # check that POST request failed
            response = self.client.post(url_for('login.register'), data=self.register_payload)
            self.assertEquals(response.status_code, 409)
            self.assertTemplateUsed(REGISTER_TEMPLATE_NAME)
            self.assertContext('action', url_for('login.register'))

    """
    test_register_failure_form_failure
    ----------------------------------
    Tests that posting to register fails if
    not all fields of the form are submitted
    """
    def test_register_failure_form_failure(self):
        # create a user
        self._create_user(email='ryan')

        # check that POST request failed
        bad_payload = self.register_payload.copy()
        bad_payload.pop('username')
        response = self.client.post(url_for('login.register'), data=bad_payload)
        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(REGISTER_TEMPLATE_NAME)
        self.assertContext('action', url_for('login.register'))

        # check that POST request failed
        bad_payload = self.register_payload.copy()
        bad_payload.pop('password')
        response = self.client.post(url_for('login.register'), data=bad_payload)
        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(REGISTER_TEMPLATE_NAME)
        self.assertContext('action', url_for('login.register'))

        # check that POST request failed
        bad_payload = self.register_payload.copy()
        bad_payload.pop('phone')
        response = self.client.post(url_for('login.register'), data=bad_payload)
        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(REGISTER_TEMPLATE_NAME)
        self.assertContext('action', url_for('login.register'))

    """
    test_register_success
    ---------------------
    Tests that we can register a new user successfully
    """
    def test_register_success(self):
        # replace validate_user function so it passes
        with Replacer() as r:
            r.replace('steerclear.utils.cas.validate_user', self.mock_validate_user)
            # create user and check for success in response
            response = self.client.post(url_for('login.register'), data=self.register_payload)
            self.assertRedirects(response, url_for('login.login'))

            # find new user in db and check that it has correct email/password
            user = User.query.filter_by(email=self.register_payload[u'username']).first()
            self.assertIsNotNone(user)
            self.assertEquals(user.email, self.register_payload[u'username'])
            self.assertEquals(user.phone.e164, self.register_payload[u'phone'])
            self.assertEquals(user.roles.all(), [self.student_role])

            # make sure we can log in as new user
            response = self.client.post(url_for('login.login'), data=self.register_payload)
            self.assertRedirects(response, url_for('driver_portal.index'))
