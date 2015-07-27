from steerclear import app
from steerclear.forms import UserForm
import unittest, flask

# email string min and max lengths
EMAIL_MIN_LENGTH = 1
EMAIL_MAX_LENGTH = 119

# password string min and max lengths
PASSWORD_MIN_LENGTH = 1
PASSWORD_MAX_LENGTH = 119

"""
UserFormTestCase
----------------
Tests for login module UserForm
"""
class UserFormTestCase(unittest.TestCase):

    """
    submit_form
    -----------
    helper method to submit a UserForm by faking
    a request context. Returns True is the form
    validated and False if not.

    *payload* is a dictionary of name/value pairs
              of the form data that is being submitted
    """
    def submit_form(self, payload):
        with app.test_request_context():
            form = UserForm(data=payload)
            return form.validate()

    def setUp(self):
        self.payload = {
            u"email": u"ryan",
            u"password": u"1234",
        }

    """
    test_ride_form_correct_submit
    -----------------------------
    Tests that a UserForm can be validated correctly
    """
    def test_ride_form_correct_submit(self):
        result = self.submit_form(self.payload)
        self.assertTrue(result)

    """
    test_data_required_fields
    -------------------------
    tests that a UserForm is not valid unless
    all fields are included in the form data
    """
    def test_data_required_fields(self):
        payload = self.payload
        for key in payload.keys():
            bad_payload = payload.copy()
            bad_payload.pop(key, None)
            result = self.submit_form(bad_payload)
            self.assertFalse(result)

    """
    test_email_min_length
    ------------------------
    Tests that a UserForm validates the minimum length
    for the email field correctly
    """
    def test_email_min_length(self):
        payload = self.payload.copy()
        payload[u'email'] = 'x' * EMAIL_MIN_LENGTH
        result = self.submit_form(payload)
        self.assertTrue(result)

        payload = self.payload.copy()
        payload[u'email'] = 'x' * (EMAIL_MIN_LENGTH-1)
        result = self.submit_form(payload)
        self.assertFalse(result)

    """
    test_email_max_length
    ------------------------
    Tests that a UserForm validates the maximum length
    for the email field correctly
    """
    def test_email_max_length(self):
        payload = self.payload.copy()
        payload[u'email'] = 'x' * EMAIL_MAX_LENGTH
        result = self.submit_form(payload)
        self.assertTrue(result)

        payload = self.payload.copy()
        payload[u'email'] = 'x' * (EMAIL_MAX_LENGTH+1)
        result = self.submit_form(payload)
        self.assertFalse(result)

    """
    test_password_min_length
    ------------------------
    Tests that a UserForm validates the minimum length
    for the password field correctly
    """
    def test_password_min_length(self):
        payload = self.payload.copy()
        payload[u'password'] = 'x' * PASSWORD_MIN_LENGTH
        result = self.submit_form(payload)
        self.assertTrue(result)

        payload = self.payload.copy()
        payload[u'password'] = 'x' * (PASSWORD_MIN_LENGTH-1)
        result = self.submit_form(payload)
        self.assertFalse(result)

    """
    test_password_max_length
    ------------------------
    Tests that a UserForm validates the maximum length
    for the password field correctly
    """
    def test_password_max_length(self):
        payload = self.payload.copy()
        payload[u'password'] = 'x' * PASSWORD_MAX_LENGTH
        result = self.submit_form(payload)
        self.assertTrue(result)

        payload = self.payload.copy()
        payload[u'password'] = 'x' * (PASSWORD_MAX_LENGTH+1)
        result = self.submit_form(payload)
        self.assertFalse(result)
