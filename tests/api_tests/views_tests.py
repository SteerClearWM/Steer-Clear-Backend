from steerclear import app, db
from steerclear.models import Ride
from steerclear.api.views import query_distance_matrix_api
from tests.base import base

from testfixtures import replace, test_datetime
from flask import url_for
from datetime import datetime, timedelta
import vcr

# vcr object used to record api request responses or return already recorded responses
myvcr = vcr.VCR(cassette_library_dir='tests/fixtures/vcr_cassettes/api_tests/')

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

    """
    test_get_ride_list_requires_login
    ---------------------------------
    Tests that getting the list of ride requests
    requires that the user be logged in
    """
    def test_get_ride_list_requires_login(self):
        response = self.client.get(url_for('api.rides'))
        self.assertEquals(response.status_code, 401)

    """
    test_get_ride_list_requires_admin_permission
    ---------------------------------------------------
    Tests that trying to access the GET RideList API requires
    the User to be a admin
    """
    def test_get_ride_list_requires_admin_permission(self):
        self._test_url_requires_roles(
            self.client.get,
            url_for('api.rides'),
            [self.admin_role]
        )

    """
    test_get_ride_list_empty_list
    ---------------
    Tests that listing all of the rides in the queue is correct.
    """
    def test_get_ride_list_empty_list(self):
        self._login(self.admin_user)
        response = self.client.get(url_for('api.rides'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json, {"rides": []})

    """
    test_get_ride_list_not_empty_list
    -------------------------
    Tests that api can return the rides list correctly when
    the queue is not empty
    """
    def test_get_ride_list_not_empty_list(self):
        self._login(self.admin_user)
        # create ride objects
        r1 = self._create_ride(self.admin_user)
        r2 = self._create_ride(self.admin_user)
        r3 = self._create_ride(self.admin_user)
        
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
        self.assertEquals(response.json, {'rides': [r1_dict, r2_dict, r3_dict]})

    """
    test_get_ride_list_filter_by_location
    -------------------------------------
    Tests that using the filter query string 'location'
    correctly filters the ride request queue
    """
    def test_get_ride_list_filter_by_location(self):
        self._login(self.admin_user)

        # create and save some off campus and on campus ride requests
        n = 6
        on_campus_rides = []
        off_campus_rides = []
        for _ in xrange(n):
            on_campus_rides.append(self._create_ride(self.admin_user, on_campus=True))
            off_campus_rides.append(self._create_ride(self.admin_user, on_campus=False))

        # create 1 extra on campus ride just to have imbalance
        on_campus_rides.append(self._create_ride(self.admin_user, on_campus=True))

        # check that filtering by on campus rides only returns
        # ride requests that were on campus
        response = self.client.get(url_for('api.rides', location='on_campus'))
        rides = response.json['rides']
        for ride in rides:
            # every ride in response should be on campus
            self.assertTrue(ride['on_campus'])
        # there should be n+1 number of rides on campus
        self.assertEqual(len(rides), n+1)

        # check that filtering by off campus rides only returns
        # ride requests that were off campus
        response = self.client.get(url_for('api.rides', location='off_campus'))
        rides = response.json['rides']
        for ride in rides:
            # every ride in response should be off campus
            self.assertFalse(ride['on_campus'])
        # there should be n number of rides off campus
        self.assertEquals(len(rides), n)

        # check that putting a random value for 'location' returns
        # all current ride requests
        response = self.client.get(url_for('api.rides', location='foobar'))
        rides = response.json['rides']
        on_campus_count = 0
        off_campus_count = 0
        for ride in rides:
            # count the number of on campus and off campus rides in response
            if ride['on_campus']:
                on_campus_count += 1
            else:
                off_campus_count += 1
        # there should be n+n+1 number of rides,
        # n+1 number of on campus rides,
        # and n number of off campus rides
        self.assertEquals(len(rides), n+n+1)
        self.assertEquals(on_campus_count, n+1)
        self.assertEquals(off_campus_count, n)

        # check that omitting 'location' returns all rides
        response = self.client.get(url_for('api.rides'))
        rides = response.json['rides']
        on_campus_count = 0
        off_campus_count = 0
        for ride in rides:
            # count the number of on campus and off campus rides in response
            if ride['on_campus']:
                on_campus_count += 1
            else:
                off_campus_count += 1
        # there should be n+n+1 number of rides,
        # n+1 number of on campus rides,
        # and n number of off campus rides
        self.assertEquals(len(rides), n+n+1)
        self.assertEquals(on_campus_count, n+1)
        self.assertEquals(off_campus_count, n)

    """
    test_post_ride_list_requires_login
    ----------------------------------
    Tests that the user must be logged in in order to
    create a new ride request
    """
    def test_post_ride_list_requires_login(self):
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
        self._login(self.student_user)
        travel_time = 239
        expected_pickup_time = datetime(2015,6,13,1,2,3) + timedelta(0, 10 * 60)
        expected_dropoff_time = expected_pickup_time + timedelta(0, travel_time)
        expected_pickup_string = expected_pickup_time.strftime('%a, %d %b %Y %H:%M:%S -0000')
        expected_dropoff_string = expected_dropoff_time.strftime('%a, %d %b %Y %H:%M:%S -0000')
        payload = {
            u"num_passengers": 3,
            u"start_latitude": 37.2735,
            u"start_longitude": -76.7196,
            u"end_latitude": 37.2809,
            u"end_longitude": -76.7197,
            u"pickup_time": expected_pickup_string,
            u"travel_time": travel_time,
            u"dropoff_time": expected_dropoff_string,
            u'pickup_address': u'2006 Brooks Street, Williamsburg, VA 23185, USA',
            u'dropoff_address': u'1234 Richmond Road, Williamsburg, VA 23185, USA',
            u'on_campus': True
          }

        response = self.client.post(url_for('api.rides'), data=payload)
        payload[u'id'] = 1
        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.json, {u"ride": payload})
        self.assertEquals(Ride.query.get(1).user, self.student_user)

    """
    test_post_ride_list_bad_form_data
    ---------------------------------
    Tests that trying to create a new ride fails if
    required fields are not in form
    """
    def test_post_ride_list_bad_form_data(self):
        self._login(self.student_user)
        payload = {
            u"num_passengers": 3,
            u"start_latitude": 37.273485,
            u"start_longitude": -76.719628,
            u"end_latitude": 37.280893,
            u"end_longitude": -76.719691,
          }

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

    """
    test_get_ride_requires_login
    ----------------------------
    Tests that user must be logged in to access a ride request
    """
    def test_get_ride_requires_login(self):
        response = self.client.get(url_for('api.ride', ride_id=0))
        self.assertEquals(response.status_code, 401)

    """
    test_get_ride_requires_student_or_admin_permission
    ---------------------------------------------------
    Tests that trying to access the get Ride API requires
    the User to be a student or an admin
    """
    def test_get_ride_requires_student_or_admin_permission(self):
        # Create ride so that we try to get an existing ride
        self._create_ride(self.student_user)
        self._test_url_requires_roles(
            self.client.get, 
            url_for('api.ride', ride_id=1),
            [self.student_role, self.admin_role]
        )

    """
    test_get_ride_bad_ride_id
    --------------------------
    Tests that trying to get a specific ride with
    a bad ride id returns 404
    """
    def test_get_ride_bad_ride_id(self):
        self._login(self.student_user)
        # check that bad ride_id get request returns 404
        response = self.client.get(url_for('api.ride', ride_id=1))
        self.assertEquals(response.status_code, 403)

        ride = self._create_ride(self.student_user)

        # check that bad ride_id with not empty database returns 404
        response = self.client.get(url_for('api.ride', ride_id=2))
        self.assertEquals(response.status_code, 403)

        # finally, check that good ride_id, doesn't return 403/404
        response = self.client.get(url_for('api.ride', ride_id=1))
        self.assertEquals(response.status_code, 200)

    """
    test_get_ride_success
    ----------------------
    Tests that api successfully gets a specified
    ride object given its ride_id
    """
    def test_get_ride_success(self):
        self._login(self.student_user)
        # create ride objects to db
        r1 = self._create_ride(self.student_user)
        r2 = self._create_ride(self.student_user)
        r3 = self._create_ride(self.student_user)
        
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
        self.assertEquals(response.json, {'ride': r1_dict})

        response = self.client.get(url_for('api.ride', ride_id=2))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json, {'ride': r2_dict})

        response = self.client.get(url_for('api.ride', ride_id=3))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json, {'ride': r3_dict})

    """
    test_get_ride_can_only_get_accessible_ride
    ------------------------------------------
    Tests that Users can only access the GET RideAPI for
    Ride requests they have made
    """
    def test_get_ride_can_only_get_accessible_ride(self):
        # create 2 Ride objects by 2 different students
        self._create_ride(self.student_user)
        self._create_ride(self.student_user2)

        # login first student
        self._login(self.student_user)

        # check that first student can access the ride they placed
        response = self.client.get(url_for('api.ride', ride_id=1))
        self.assertEquals(response.status_code, 200)

        # check that first student cannot access any rides they didn't place
        response = self.client.get(url_for('api.ride', ride_id=2))
        self.assertEquals(response.status_code, 403)

        # login second student
        self._login(self.student_user2)

        # check that the second student cannot access any rides they didn't place
        response = self.client.get(url_for('api.ride', ride_id=1))
        self.assertEquals(response.status_code, 403)

        # check that the second student can access the ride they placed
        response = self.client.get(url_for('api.ride', ride_id=2))
        self.assertEquals(response.status_code, 200)

    """
    test_delete_ride_requires_login
    -------------------------------
    Tests that a user must be logged in to delete a ride request
    """
    def test_delete_ride_requires_login(self):
        response = self.client.delete(url_for('api.ride', ride_id=0))
        self.assertEquals(response.status_code, 401)

    """
    test_delete_ride_requires_student_or_admin_permission
    ---------------------------------------------------
    Tests that trying to access the delete Ride API requires
    the User to be a student or an admin
    """
    def test_delete_ride_requires_student_or_admin_permission(self):
        # Create ride so that we try to get an existing ride
        self._create_ride(self.student_user)
        self._test_url_requires_roles(
            self.client.delete,
            url_for('api.ride', ride_id=1),
            [self.student_role, self.admin_role]
        )

    """
    test_delete_ride_bad_ride_id
    -----------------------------
    Test that api returns 404 to a ride id that doesn't exist
    """
    def test_delete_ride_bad_ride_id(self):
        self._login(self.student_user)
        # check that bad ride_id delete request returns 404
        response = self.client.delete(url_for('api.ride', ride_id=1))
        self.assertEquals(response.status_code, 403)

        ride = self._create_ride(self.student_user)

        # check that bad ride_id with not empty database returns 404
        response = self.client.delete(url_for('api.ride', ride_id=2))
        self.assertEquals(response.status_code, 403)

        # finally check to see that accessing the ride object doesn't fail
        response = self.client.delete(url_for('api.ride', ride_id=1))
        self.assertEquals(response.status_code, 204)

    """
    test_delete_ride_success
    -------------------------
    Tests that deleting a ride works
    """
    def test_delete_ride_success(self):
        self._login(self.student_user)
        # create Ride objects
        r1 = self._create_ride(self.student_user)
        r2 = self._create_ride(self.student_user)
        r3 = self._create_ride(self.student_user)

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
    test_delete_ride_can_only_delete_accessible_ride
    ------------------------------------------
    Tests that Users can only access the DELETE RideAPI for
    Ride requests they have made
    """
    def test_delete_ride_can_only_delete_accessible_ride(self):
        # create 2 Ride objects by 2 different students
        self._create_ride(self.student_user)
        self._create_ride(self.student_user2)

        # login first student
        self._login(self.student_user)

        # check that first student can delete the ride they placed
        response = self.client.delete(url_for('api.ride', ride_id=1))
        self.assertEquals(response.status_code, 204)

        # check that first student cannot delete any rides they didn't place
        response = self.client.delete(url_for('api.ride', ride_id=2))
        self.assertEquals(response.status_code, 403)

        # create another ride by the first student
        self._create_ride(self.student_user)

        # login second student
        self._login(self.student_user2)

        # check that the second student cannot delete any rides they didn't place
        response = self.client.delete(url_for('api.ride', ride_id=3))
        self.assertEquals(response.status_code, 403)

        # check that the second student can delete the ride they placed
        response = self.client.delete(url_for('api.ride', ride_id=2))
        self.assertEquals(response.status_code, 204)


"""
NotificationAPITestCase
-----------------------
Test case for testing the notifications api
"""
class NotificationAPITestCase(base.SteerClearBaseTestCase):

    """
    setUp
    -----
    Overrides super class setUp(). Makes sure the user
    is logged in before each test is run
    """
    def setUp(self):
        super(NotificationAPITestCase, self).setUp()

    """
    test_post_notifications_requires_login
    --------------------------------------
    Tests that the notifications route requires the user to be logged in
    """
    def test_post_notifications_requires_login(self):
        response = self.client.post(url_for('api.notifications'), data={})
        self.assertEquals(response.status_code, 401)

    """
    test_post_notifications_requires_admin_permission
    ---------------------------------------------------
    Tests that trying to access the notifications API requires
    the User to be a admin
    """
    def test_post_notifications_requires_admin_permission(self):
        self._test_url_requires_roles(
            self.client.post,
            url_for('api.notifications'),
            [self.admin_role]
        )    

    """
    test_post_notifications_bad_ride_id
    -----------------------------------
    Tests that the notifications route fails if the
    request ride_id does not exist
    """
    def test_post_notifications_bad_ride_id(self):
        self._login(self.admin_user)
        response = self.client.post(url_for('api.notifications'), data={'ride_id': 1})
        self.assertEquals(response.status_code, 400)

        ride = self._create_ride(self.student_user)

        response = self.client.post(url_for('api.notifications'), data={'ride_id': 2})
        self.assertEquals(response.status_code, 400)


"""
ETAAPITestCase
------------------
TestCase for testing API interface with eta calculation module
"""
class ETAAPITestCase(base.SteerClearBaseTestCase):

    @myvcr.use_cassette()
    @replace('steerclear.api.views.datetime', test_datetime(2015,6,13,1,2,3))
    def test_query_distance_matrix_api_no_rides(self):
        pickup_loc = (37.273485, -76.719628)
        dropoff_loc = (37.280893, -76.719691)
        expected_pickup_time = datetime(2015,6,13,1,2,3) + timedelta(0, 10 * 60)
        expected_dropoff_time = expected_pickup_time + timedelta(0, 239)
        result = query_distance_matrix_api(pickup_loc, dropoff_loc)

        (pickup_time, travel_time, dropoff_time) = result[0]
        self.assertEquals(pickup_time, expected_pickup_time)
        self.assertEquals(travel_time, 239)
        self.assertEquals(dropoff_time, expected_dropoff_time)

        pickup_address, dropoff_address = result[1]
        self.assertEquals(pickup_address, u'2006 Brooks Street, Williamsburg, VA 23185, USA')
        self.assertEquals(dropoff_address, u'1234 Richmond Road, Williamsburg, VA 23185, USA')

    @myvcr.use_cassette()
    def test_query_distance_matrix_api_no_rides_bad_pickup_loc(self):
        pickup_loc = (0.0, 0.0)
        dropoff_loc = (37.280893, -76.719691)
        result = query_distance_matrix_api(pickup_loc, dropoff_loc)
        self.assertEquals(result, None)

    @myvcr.use_cassette()
    def test_query_distance_matrix_api_no_rides_bad_dest_loc(self):
        pickup_loc = (37.280893, -76.719691)
        dropoff_loc = (0.0, 0.0)
        result = query_distance_matrix_api(pickup_loc, dropoff_loc)
        self.assertEquals(result, None)

    @myvcr.use_cassette()
    def test_query_distance_matrix_api_with_last_ride(self):
        user = self._create_user()
        ride = self._create_ride(user, 1, 0.0, 0.0, 37.272042, -76.714027, dropoff_time=datetime(2015,6,13,1,2,3))
        pickup_loc = (37.273485, -76.719628)
        dropoff_loc = (37.280893, -76.719691)
        expected_pickup_time = datetime(2015,6,13,1,2,3) + timedelta(0, 373)
        expected_travel_time = 239
        expected_dropoff_time = expected_pickup_time + timedelta(0, expected_travel_time)
        result = query_distance_matrix_api(pickup_loc, dropoff_loc)

        (pickup_time, travel_time, dropoff_time) = result[0]
        self.assertEquals(pickup_time, expected_pickup_time)
        self.assertEquals(travel_time, expected_travel_time)
        self.assertEquals(dropoff_time, expected_dropoff_time)

        pickup_address, dropoff_address = result[1]
        self.assertEquals(pickup_address, u'2006 Brooks Street, Williamsburg, VA 23185, USA')
        self.assertEquals(dropoff_address, u'1234 Richmond Road, Williamsburg, VA 23185, USA') 

    @myvcr.use_cassette()
    def test_query_distance_matrix_api_with_last_ride_bad_pickup_loc(self):
        user = self._create_user()
        self._create_ride(user, 1, 0.0, 0.0, 37.272042, -76.714027, dropoff_time=datetime(2015,6,13,1,2,3))
        pickup_loc = (0.0, 0.0)
        dropoff_loc = (37.280893, -76.719691)
        result = query_distance_matrix_api(pickup_loc, dropoff_loc)
        self.assertEquals(result, None)   

    @myvcr.use_cassette()
    def test_query_distance_matrix_api_with_last_ride_bad_dropoff_loc(self):
        user = self._create_user()
        self._create_ride(user, 1, 0.0, 0.0, 37.272042, -76.714027, dropoff_time=datetime(2015,6,13,1,2,3))
        pickup_loc = (37.280893, -76.719691)
        dropoff_loc = (0.0, 0.0)
        result = query_distance_matrix_api(pickup_loc, dropoff_loc)
        self.assertEquals(result, None)
