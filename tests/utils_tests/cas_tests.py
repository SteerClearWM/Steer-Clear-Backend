from steerclear.utils.cas import *
from steerclear import app
import unittest, vcr

# vcr object used to record api request responses or return already recorded responses
myvcr = vcr.VCR(cassette_library_dir='tests/fixtures/vcr_cassettes/cas_tests/')

"""
CASTestCase
-----------
Tests for validating users against the W&M CAS server
"""
class CASTestCase(unittest.TestCase):

    def setUp(self):
        self.username = app.config['TEST_CAS_USERNAME']
        self.password = app.config['TEST_CAS_PASSWORD']

    """
    test_validate_user_empty_username_and_password
    ----------------------------------------------
    Tests that validation fails with empty credentials
    """
    @myvcr.use_cassette()
    def test_validate_user_empty_username_and_password(self):
        result = validate_user('', '')
        self.assertFalse(result)

    """
    test_validate_user_bad_password
    ----------------------------------------------
    Tests that validation fails with bad password
    """
    @myvcr.use_cassette()
    def test_validate_user_bad_password(self):
        result = validate_user(self.username, 'password')
        self.assertFalse(result)

    """
    test_validate_user_bad_username
    ----------------------------------------------
    Tests that validation fails with bad username
    """
    @myvcr.use_cassette()
    def test_validate_user_bad_username(self):
        result = validate_user('username', self.password)
        self.assertFalse(result) 

    """
    test_validate_user_success
    ----------------------------------------------
    Tests that validation succeeds with valid credentials
    """
    @myvcr.use_cassette()
    def test_validate_user_success(self):
        result = validate_user(self.username, self.password)
        self.assertTrue(result)

