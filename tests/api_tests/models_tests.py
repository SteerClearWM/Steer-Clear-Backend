from steerclear import app, db
from steerclear.models import Ride
from tests.base import base

from datetime import datetime
import json

# format string for Ride.__repr__()
RIDE_REPR_STRING = '<Ride(ID %r, Passengers %r, Pickup <%r, %r>, Dropoff <%r, %r>, ETP %r, Duration %r, ETD %r)>'

"""
RideModelTestCase
-----------------
Test case for testing the Ride Model
"""
class RideModelTestCase(base.SteerClearBaseTestCase):

    """
    setUp
    -----
    Call super class setUp() and create default Ride object
    """
    def setUp(self):
        super(RideModelTestCase, self).setUp()
        self.user = self._create_user()
        self.default_ride = self._create_ride(self.user)

    """
    test_as_dict
    ------------
    Tests that the Ride Model's as_dict() method is correct
    """
    def test_as_dict(self):
        correct_default_dict = {
            'id': 1,
            'num_passengers': 0, 
            'start_latitude': 1.0, 
            'start_longitude': 1.1, 
            'end_latitude': 2.0, 
            'end_longitude': 2.1, 
            'pickup_time': datetime(1,1,1), 
            'travel_time': 10, 
            'dropoff_time': datetime(1,1,1)
        }
        self.assertEquals(self.default_ride.as_dict(), correct_default_dict)

    """
    test_repr
    ---------
    Tests Ride models' __repr__() method
    """
    def test_repr(self):
        correct_default_repr = RIDE_REPR_STRING % (1, 0, 1.0, 1.1, 2.0, 2.1, datetime(1,1,1), 10, datetime(1,1,1))
        self.assertEquals(self.default_ride.__repr__(), correct_default_repr)

