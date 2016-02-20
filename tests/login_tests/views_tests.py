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
    test_login_failure_incorrect_username
    -------------------------------------
    Tests that login fails if the user supplies the wrong username
    """
    def test_login_failure_incorrect_username(self):
        # replace validate_user function so it passes
        with Replacer() as r:
            r.replace('steerclear.utils.cas.validate_user', self.mock_validate_user)
            
            # test with no Users in db
            response = self.client.post(url_for('login.login'), data=self.login_payload)
            self.assertTemplateUsed(LOGIN_TEMPLATE_NAME)
            self.assertEquals(response.status_code, 400)

            # test with user that has different username but same password
            self._create_user(username='kyle')
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
        def mock_validate(username, password):
            return False
        # replace validate_user function so it passes
        with Replacer() as r:
            r.replace('steerclear.utils.cas.validate_user', mock_validate)
            
            # test with no Users in db
            response = self.client.post(url_for('login.login'), data=self.login_payload)
            self.assertTemplateUsed(LOGIN_TEMPLATE_NAME)
            self.assertEquals(response.status_code, 400)

            # test with user that has same username but different password
            self._create_user(username='ryan')
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
            self._create_user(username='ryan')
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
            self._create_user(username='ryan')
            self.client.post(url_for('login.login'), data=self.login_payload)

            # logout user
            response = self.client.get(url_for('login.logout'))
            self.assertRedirects(response, url_for('login.login'))

            # make sure we are actually loged out
            response = self.client.get(url_for('login.logout'))
            self.assertEquals(response.status_code, 401)

    """
    test_register_failure_username_exists
    -------------------------------------
    Tests that trying to register a new user with
    a username that already exists fails
    """
    def test_register_failure_username_exists(self):
        # replace validate_user function so it passes
        with Replacer() as r:
            r.replace('steerclear.utils.cas.validate_user', self.mock_validate_user)
            # create a user
            self._create_user(username='ryan')

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
        self._create_user(username='ryan')

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

            # find new user in db and check that it has correct username/password
            user = User.query.filter_by(username=self.register_payload[u'username']).first()
            self.assertIsNotNone(user)
            self.assertEquals(user.username, self.register_payload[u'username'])
            self.assertEquals(user.phone.e164, self.register_payload[u'phone'])
            self.assertEquals(user.roles, [self.student_role])

            # make sure we can log in as new user
            response = self.client.post(url_for('login.login'), data=self.register_payload)
            self.assertRedirects(response, url_for('driver_portal.index'))
