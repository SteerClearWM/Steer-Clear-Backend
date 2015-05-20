from steerclear import app
from steerclear.forms import RideForm
from steerclear.models import *
import unittest, flask

"""
RideFormTestCase
----------------
Test class for the RideForm class
"""
class RideFormTestCase(unittest.TestCase):

    """
    submit_form
    -----------
    helper method to submit a RideForm by faking
    a request context. Returns True is the form
    validated and False if not.

    *payload* is a dictionary of name/value pairs
              of the form data that is being submitted
    """
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

    """
    test_ride_form_correct_submit
    -----------------------------
    Tests that a RideForm can be validated correctly
    """
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

    """
    test_num_passengers_min_range
    -----------------------------
    Tests that a RideForm accepts the correct min
    range value for the 'num_passengers' field
    """
    def test_num_passengers_min_range(self):
        payload = self.payload.copy()
        payload[u'num_passengers'] = 1
        result = self.submit_form(payload)
        self.assertTrue(result)

    """
    test_num_passengers_max_range
    -----------------------------
    Tests that a RideForm accepts the correct max
    range value for the 'num_passengers' field
    """
    def test_num_passengers_max_range(self):
        payload = self.payload.copy()
        payload[u'num_passengers'] = 8
        result = self.submit_form(payload)
        self.assertTrue(result)

    """
    test_num_passengers_bad_range
    -----------------------------
    Tests that a RideForm does not accept values
    for the 'num_passengers' field that are out of range
    """
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

    """
    test_as_ride
    ------------
    Tests that RideForm.as_dict can convert a valid 
    RideForm to the correct Ride object.
    """
    def test_as_ride(self):
        payload = self.payload.copy()
        form_ride = None
        with app.test_request_context():
            form = RideForm(data=payload)
            form_ride = form.as_ride()
        ride = Ride(
                payload[u'num_passengers'],
                (payload[u'start_latitude'], payload[u'start_longitude']),
                (payload[u'end_latitude'], payload[u'end_longitude'])
            )

        self.assertEquals(form_ride.as_dict(), ride.as_dict())

