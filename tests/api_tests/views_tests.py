from steerclear import app, db
from steerclear.models import Ride
from steerclear.api.views import calculate_time_data
from tests.base import base

from testfixtures import replace, test_datetime
from flask import url_for
from datetime import datetime, timedelta
import json, vcr

# vcr object used to record api request responses or return already recorded responses
myvcr = vcr.VCR(cassette_library_dir='tests/fixtures/vcr_cassettes/eta_tests/')

"""
RideListAPITestCase
-------------------
Test cases for the RideListAPI class that deals with managing and
interacting with the list of ride requests
"""
class RideListAPITestCase(base.SteerClearBaseTestCase):

    """
    setUp
    -----
    Overrides base test case setUp(). makes sure
    The user is logged in before each test is run
    """
    def setUp(self):
        super(RideListAPITestCase, self).setUp()
        self._login()

    """
    test_get_ride_list_requires_login
    ---------------------------------
    Tests that getting the list of ride requests
    requires that the user be logged in
    """
    def test_get_ride_list_requires_login(self):
        self._logout()
        response = self.client.get(url_for('api.rides'))
        self.assertEquals(response.status_code, 401)

    """
    test_get_ride_list_empty_list
    ---------------
    Tests that listing all of the rides in the queue is correct.
    """
    def test_get_ride_list_empty_list(self):
        response = self.client.get(url_for('api.rides'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.get_data()), {"rides": []})

    """
    test_get_ride_list_not_empty_list
    -------------------------
    Tests that api can return the rides list correctly when
    the queue is not empty
    """
    def test_get_ride_list_not_empty_list(self):
        # create ride objects
        r1 = self._create_ride()
        r2 = self._create_ride()
        r3 = self._create_ride()
        
        # store dict versions
        r1_dict = r1.as_dict()
        r2_dict = r2.as_dict()                     
        r3_dict = r3.as_dict()
        
        # assign correct id and time vals
        r1_dict['pickup_time'] = 'Mon, 01 Jan 0001 00:00:00 -0000'
        r2_dict['pickup_time'] = 'Mon, 01 Jan 0001 00:00:00 -0000'
        r3_dict['pickup_time'] = 'Mon, 01 Jan 0001 00:00:00 -0000'
        r1_dict['dropoff_time'] = 'Mon, 01 Jan 0001 00:00:00 -0000'
        r2_dict['dropoff_time'] = 'Mon, 01 Jan 0001 00:00:00 -0000'
        r3_dict['dropoff_time'] = 'Mon, 01 Jan 0001 00:00:00 -0000'

        # test response
        response = self.client.get(url_for('api.rides'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.get_data()), {'rides': [r1_dict, r2_dict, r3_dict]})

    """
    test_post_ride_list_requires_login
    ----------------------------------
    Tests that the user must be logged in in order to
    create a new ride request
    """
    def test_post_ride_list_requires_login(self):
        self._logout()
        response = self.client.post(url_for('api.rides'), data={})
        self.assertEquals(response.status_code, 401)

    """
    test_post_ride_list
    -------------
    Tests that adding a new ride request works. Sends POST ride
    request data to '/rides/' and checks if the response json object
    is a valid ride request
    """
    @myvcr.use_cassette()
    @replace('steerclear.api.views.datetime', test_datetime(2015,6,13,1,2,3))
    def test_post_ride_list(self):
        expected_pickup_time = datetime(2015,6,13,1,2,3) + timedelta(0, 10 * 60)
        expected_dropoff_time = expected_pickup_time + timedelta(0, 171)
        expected_pickup_string = expected_pickup_time.strftime('%a, %d %b %Y %H:%M:%S -0000')
        expected_dropoff_string = expected_dropoff_time.strftime('%a, %d %b %Y %H:%M:%S -0000')
        payload = {
                    u"num_passengers": 3,
                    u"start_latitude": 37.273485,
                    u"start_longitude": -76.719628,
                    u"end_latitude": 37.280893,
                    u"end_longitude": -76.719691,
                    u"pickup_time": expected_pickup_string,
                    u"travel_time": 171,
                    u"dropoff_time": expected_dropoff_string,
                  }
        response = self.client.post(url_for('api.rides'), data=payload)
        payload[u'id'] = 1
        self.assertEquals(response.status_code, 201)
        self.assertEquals(json.loads(response.get_data()), {u"ride": payload})

        bad_payload = payload.copy()
        bad_payload.pop('num_passengers', None)
        bad_payload.pop('id', None)
        r = self.client.post(url_for('api.rides'), data=bad_payload)
        self.assertEquals(r.status_code, 400)

        bad_payload = payload.copy()
        bad_payload.pop('start_latitude', None)
        bad_payload.pop('id', None)
        r = self.client.post(url_for('api.rides'), data=bad_payload)
        self.assertEquals(r.status_code, 400)

        bad_payload = payload.copy()
        bad_payload.pop('start_longitude', None)
        bad_payload.pop('id', None)
        r = self.client.post(url_for('api.rides'), data=bad_payload)
        self.assertEquals(r.status_code, 400)

        bad_payload = payload.copy()
        bad_payload.pop('end_latitude', None)
        bad_payload.pop('id', None)
        r = self.client.post(url_for('api.rides'), data=bad_payload)
        self.assertEquals(r.status_code, 400)

        bad_payload = payload.copy()
        bad_payload.pop('end_longitude', None)
        bad_payload.pop('id', None)
        r = self.client.post(url_for('api.rides'), data=bad_payload)
        self.assertEquals(r.status_code, 400)


"""
RideAPITestCase
---------------
Test Cases for the RideAPI class that deals with
managing and interacting with individual Ride objects
"""
class RideAPITestCase(base.SteerClearBaseTestCase):

    """
    setUp
    -----
    Overrides super class setUp(). Makes sure the user
    is logged in before each test is run
    """
    def setUp(self):
        super(RideAPITestCase, self).setUp()
        self._login()

    """
    test_get_ride_requires_login
    ----------------------------
    Tests that user must be logged in to access a ride request
    """
    def test_get_ride_requires_login(self):
        self._logout()
        response = self.client.get(url_for('api.ride', ride_id=0))
        self.assertEquals(response.status_code, 401)

    """
    test_get_ride_bad_ride_id
    --------------------------
    Tests that trying to get a specific ride with
    a bad ride id returns 404
    """
    def test_get_ride_bad_ride_id(self):
        # check that bad ride_id get request returns 404
        response = self.client.get(url_for('api.ride', ride_id=0))
        self.assertEquals(response.status_code, 404)

        ride = self._create_ride()

        # check that bad ride_id with not empty database returns 404
        response = self.client.get(url_for('api.ride', ride_id=2))
        self.assertEquals(response.status_code, 404)

    """
    test_get_ride_success
    ----------------------
    Tests that api successfully gets a specified
    ride object given its ride_id
    """
    def test_get_ride_success(self):
        # create ride objects to db
        r1 = self._create_ride()
        r2 = self._create_ride()
        r3 = self._create_ride()
        
        # store dict versions
        r1_dict = r1.as_dict()                             
        r2_dict = r2.as_dict()                     
        r3_dict = r3.as_dict()
        
        # assign correct id vals
        r1_dict[u'pickup_time'] = u'Mon, 01 Jan 0001 00:00:00 -0000'
        r2_dict[u'pickup_time'] = u'Mon, 01 Jan 0001 00:00:00 -0000'
        r3_dict[u'pickup_time'] = u'Mon, 01 Jan 0001 00:00:00 -0000'
        r1_dict[u'dropoff_time'] = u'Mon, 01 Jan 0001 00:00:00 -0000'
        r2_dict[u'dropoff_time'] = u'Mon, 01 Jan 0001 00:00:00 -0000'
        r3_dict[u'dropoff_time'] = u'Mon, 01 Jan 0001 00:00:00 -0000'

        response = self.client.get(url_for('api.ride', ride_id=1))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.get_data()), {'ride': r1_dict})

        response = self.client.get(url_for('api.ride', ride_id=2))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.get_data()), {'ride': r2_dict})

        response = self.client.get(url_for('api.ride', ride_id=3))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.get_data()), {'ride': r3_dict})

    """
    test_delete_ride_requires_login
    -------------------------------
    Tests that a user must be logged in to delete a ride request
    """
    def test_delete_ride_requires_login(self):
        self._logout()
        response = self.client.delete(url_for('api.ride', ride_id=0))
        self.assertEquals(response.status_code, 401)

    """
    test_delete_ride_bad_ride_id
    -----------------------------
    Test that api returns 404 to a ride id that doesn't exist
    """
    def test_delete_ride_bad_ride_id(self):
        # check that bad ride_id delete request returns 404
        response = self.client.delete(url_for('api.ride', ride_id=0))
        self.assertEquals(response.status_code, 404)

        ride = self._create_ride()

        # check that bad ride_id with not empty database returns 404
        response = self.client.delete(url_for('api.ride', ride_id=2))
        self.assertEquals(response.status_code, 404)

    """
    test_delete_ride_success
    -------------------------
    Tests that deleting a ride works
    """
    def test_delete_ride_success(self):
        # create Ride objects
        r1 = self._create_ride()
        r2 = self._create_ride()
        r3 = self._create_ride()

        # store dict versions
        r2_dict = r2.as_dict()                             
        r3_dict = r3.as_dict()

        # test can delete a ride
        response = self.client.delete(url_for('api.ride', ride_id=1))
        self.assertEquals(response.status_code, 204)
        self.assertEquals(response.data, '')
        self.assertEquals(len(Ride.query.all()), 2)
        self.assertEquals(Ride.query.get(1), None)
        self.assertEquals(Ride.query.get(2).as_dict(), r2_dict)
        self.assertEquals(Ride.query.get(3).as_dict(), r3_dict)
        
        # test can delete a ride out of order
        response = self.client.delete(url_for('api.ride', ride_id=3))
        self.assertEquals(response.status_code, 204)
        self.assertEquals(response.data, '')
        self.assertEquals(len(Ride.query.all()), 1)
        self.assertEquals(Ride.query.get(1), None)
        self.assertEquals(Ride.query.get(2).as_dict(), r2_dict)
        self.assertEquals(Ride.query.get(3), None)

        # test can delete final ride
        response = self.client.delete(url_for('api.ride', ride_id=2))
        self.assertEquals(response.status_code, 204)
        self.assertEquals(response.data, '')
        self.assertEquals(Ride.query.all(), [])
        self.assertEquals(Ride.query.get(1), None)
        self.assertEquals(Ride.query.get(2), None)
        self.assertEquals(Ride.query.get(3), None)


"""
SteerClearAPITestCase
------------------
TestCase for testing all api routes
"""
class ETATestCase(base.SteerClearBaseTestCase):

    @myvcr.use_cassette()
    @replace('steerclear.api.views.datetime', test_datetime(2015,6,13,1,2,3))
    def test_calculate_time_data_no_rides(self):
        pickup_loc = (37.273485, -76.719628)
        dropoff_loc = (37.280893, -76.719691)
        expected_pickup_time = datetime(2015,6,13,1,2,3) + timedelta(0, 10 * 60)
        expected_dropoff_time = expected_pickup_time + timedelta(0, 171)
        (pickup_time, travel_time, dropoff_time) = calculate_time_data(pickup_loc, dropoff_loc)
        self.assertEquals(pickup_time, expected_pickup_time)
        self.assertEquals(travel_time, 171)
        self.assertEquals(dropoff_time, expected_dropoff_time)

    @myvcr.use_cassette()
    def test_calculate_time_data_no_rides_bad_pickup_loc(self):
        pickup_loc = (0.0, 0.0)
        dropoff_loc = (37.280893, -76.719691)
        result = calculate_time_data(pickup_loc, dropoff_loc)
        self.assertEquals(result, None)

    @myvcr.use_cassette()
    def test_calculate_time_data_no_rides_bad_dest_loc(self):
        pickup_loc = (37.280893, -76.719691)
        dropoff_loc = (0.0, 0.0)
        result = calculate_time_data(pickup_loc, dropoff_loc)
        self.assertEquals(result, None)

    @myvcr.use_cassette()
    def test_calculate_time_data_with_last_ride(self):
        ride = self._create_ride(1, 0.0, 0.0, 37.272042, -76.714027, None, None, datetime(2015,6,13,1,2,3))
        pickup_loc = (37.273485, -76.719628)
        dropoff_loc = (37.280893, -76.719691)
        expected_pickup_time = datetime(2015,6,13,1,2,3) + timedelta(0, 252)
        expected_travel_time = 171
        expected_dropoff_time = expected_pickup_time + timedelta(0, expected_travel_time)
        (pickup_time, travel_time, dropoff_time) = calculate_time_data(pickup_loc, dropoff_loc)
        self.assertEquals(pickup_time, expected_pickup_time)
        self.assertEquals(travel_time, expected_travel_time)
        self.assertEquals(dropoff_time, expected_dropoff_time)

    @myvcr.use_cassette()
    def test_calculate_time_delta_with_last_ride_bad_start_loc(self):
        self._create_ride(1, 0.0, 0.0, 0.0, 0.0, None, None, datetime(2015,6,13,1,2,3))
        pickup_loc = (37.273485, -76.719628)
        dropoff_loc = (37.280893, -76.719691)
        result = calculate_time_data(pickup_loc, dropoff_loc)
        self.assertEquals(result, None)    

    @myvcr.use_cassette()
    def test_calculate_time_delta_with_last_ride_bad_pickup_loc(self):
        self._create_ride(1, 0.0, 0.0, 37.272042, -76.714027, None, None, datetime(2015,6,13,1,2,3))
        pickup_loc = (0.0, 0.0)
        dropoff_loc = (37.280893, -76.719691)
        result = calculate_time_data(pickup_loc, dropoff_loc)
        self.assertEquals(result, None)   

    @myvcr.use_cassette()
    def test_calculate_time_delta_with_last_ride_bad_dropoff_loc(self):
        self._create_ride(1, 0.0, 0.0, 37.272042, -76.714027, None, None, datetime(2015,6,13,1,2,3))
        pickup_loc = (37.280893, -76.719691)
        dropoff_loc = (0.0, 0.0)
        result = calculate_time_data(pickup_loc, dropoff_loc)
        self.assertEquals(result, None)   

