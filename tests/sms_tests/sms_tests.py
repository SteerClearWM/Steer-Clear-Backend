from steerclear.sms import sms
from steerclear import app
import unittest, vcr

# vcr object used to record api request responses or return already recorded responses
myvcr = vcr.VCR(cassette_library_dir='tests/fixtures/vcr_cassettes/sms_tests/')

"""
SteerClearTestCase
------------------
TestCase for twilio api interface
"""
class SteerClearTwilioTestCase(unittest.TestCase):

    """
    setUp
    -----
    called before each test function.
    """
    def setUp(self):
        self.sms_client = sms.SteerClearSMSClient(
            app.config['TWILIO_ACCOUNT_SID'], 
            app.config['TWILIO_AUTH_TOKEN'],
            app.config['TWILIO_NUMBER']
        )

    """
    test_notify_user_bad_phone_number
    ---------------------------------
    Tests that calling twilio API with bad user phone number fails
    """
    @myvcr.use_cassette()
    def test_notify_user_bad_phone_number(self):
        message = self.sms_client.notify_user("123412341234", "hello, world")
        self.assertIsNone(message)

        message = self.sms_client.notify_user("+3017778003", "hello, world")
        self.assertIsNone(message)
