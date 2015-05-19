from steerclear import app
from steerclear.forms import RideForm
import unittest, flask

class RideFormTestCase(unittest.TestCase):

    def submit_form(self, payload):
        with app.test_request_context():
            form = RideForm(data=payload)
            return form.validate()

    def setUp(self):
        self.payload = {
            u"num_passengers": 4,
            u"start_latitude": 1.1,
            u"start_longitude": 2.2,
            u"end_latitude": 3.3,
            u"end_longitude": 4.4,
        }

    def test_ride_form_correct_submit(self):
        result = self.submit_form(self.payload)
        self.assertTrue(result)

    """
    test_data_required_fields
    -------------------------
    tests that a RideForm is not valid unless
    all fields are included in the form data
    """
    def test_data_required_fields(self):
        payload = self.payload
        for key in payload.keys():
            bad_payload = payload.copy()
            bad_payload.pop(key, None)
            result = self.submit_form(bad_payload)
            self.assertFalse(result)

    def test_num_passengers_min_range(self):
        payload = self.payload.copy()
        payload[u'num_passengers'] = 1
        result = self.submit_form(payload)
        self.assertTrue(result)

    def test_num_passengers_max_range(self):
        payload = self.payload.copy()
        payload[u'num_passengers'] = 8
        result = self.submit_form(payload)
        self.assertTrue(result)

    def test_num_passengers_bad_range(self):
        bad_payload = self.payload.copy()
        bad_payload[u'num_passengers'] = 0
        result = self.submit_form(bad_payload)
        self.assertFalse(result)

        bad_payload[u'num_passengers'] = -1
        result = self.submit_form(bad_payload)
        self.assertFalse(result)

        bad_payload[u'num_passengers'] = -100
        result = self.submit_form(bad_payload)
        self.assertFalse(result)

        bad_payload[u'num_passengers'] = 9
        result = self.submit_form(bad_payload)
        self.assertFalse(result)

        bad_payload[u'num_passengers'] = 100
        result = self.submit_form(bad_payload)
        self.assertFalse(result)

