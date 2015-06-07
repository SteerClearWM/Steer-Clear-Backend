from steerclear import app, db
from steerclear.models import *
from steerclear.views import *
import unittest, json, vcr
from datetime import datetime, timedelta
from testfixtures import replace, test_datetime

# vcr object used to record api request responses or return already recorded responses
myvcr = vcr.VCR(cassette_library_dir='tests/fixtures/vcr_cassettes/eta_tests/')

"""
SteerClearTestCase
------------------
TestCase for testing all api routes
"""
class SteerClearTestCase(unittest.TestCase):

    """
    setUp
    -----
    called before each test function. Sets up flask app test
    instance and creates new test database
    """
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['TEST_SQLALCHEMY_DATABASE_URI']
        self.client = app.test_client()
        db.create_all()

    """
    tearDown
    --------
    called after each test function. breaks down test fixtures
    """
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    """
    test_heartbeat
    --------------
    tests that server is up and running and that the
    '/' route returns a 200 status code and "pulse"
    """
    def test_heartbeat(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.get_data(), "pulse")

    """
    test_list_rides
    ---------------
    Tests that listing all of the rides in the queue is correct.
    """
    def test_list_rides_empty(self):
        response = self.client.get('/rides')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.get_data()), {"rides": []})

    """
    test_list_rides_not_empty
    -------------------------
    Tests that api can return the rides list correctly when
    the queue is not empty
    """
    def test_list_rides_not_empty(self):
        dtime = datetime(1,1,1)
        r1 = Ride(1, (2.2, 3.3), (4.4, 5.5), dtime, 0, dtime) # add ride objects to db
        r2 = Ride(2, (3.3, 4.4), (5.5, 6.6), dtime, 0, dtime)
        r3 = Ride(3, (4.4, 5.5), (6.6, 7.7), dtime, 0, dtime)
        r1_dict = r1.as_dict()                             # store dict versions
        r2_dict = r2.as_dict()                     
        r3_dict = r3.as_dict()
        r1_dict['id'] = 1                                  # assign correct id vals
        r2_dict['id'] = 2
        r3_dict['id'] = 3
        r1_dict['pickup_time'] = 'Mon, 01 Jan 1 00:00:00 GMT'
        r2_dict['pickup_time'] = 'Mon, 01 Jan 1 00:00:00 GMT'
        r3_dict['pickup_time'] = 'Mon, 01 Jan 1 00:00:00 GMT'
        r1_dict['dropoff_time'] = 'Mon, 01 Jan 1 00:00:00 GMT'
        r2_dict['dropoff_time'] = 'Mon, 01 Jan 1 00:00:00 GMT'
        r3_dict['dropoff_time'] = 'Mon, 01 Jan 1 00:00:00 GMT'
        db.session.add(r1)
        db.session.add(r2)
        db.session.add(r3)
        db.session.commit()

        response = self.client.get('/rides')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.get_data()), {'rides': [r1_dict, r2_dict, r3_dict]})

    """
    test_list_ride_bad_ride_id
    --------------------------
    Tests that trying to get a specific ride with
    a bad ride id returns 404
    """
    def test_list_ride_bad_ride_id(self):
        # check that bad ride_id get request returns 404
        response = self.client.get('/rides/0')
        self.assertEquals(response.status_code, 404)

        dtime = datetime(1,1,1)
        db.session.add(Ride(1, (2.2, 3.3), (4.4, 5.5), dtime, 0, dtime))
        db.session.commit()

        # check that bad ride_id with not empty database returns 404
        response = self.client.get('/rides/2')
        self.assertEquals(response.status_code, 404)

    """
    test_list_ride_success
    ----------------------
    Tests that api successfully gets a specified
    ride object given its ride_id
    """
    def test_list_ride_success(self):
        dtime = datetime(1,1,1)
        r1 = Ride(1, (2.2, 3.3), (4.4, 5.5), dtime, 0, dtime) # add ride objects to db
        r2 = Ride(2, (3.3, 4.4), (5.5, 6.6), dtime, 0, dtime)
        r3 = Ride(3, (4.4, 5.5), (6.6, 7.7), dtime, 0, dtime)
        r1_dict = r1.as_dict()                             # store dict versions
        r2_dict = r2.as_dict()                     
        r3_dict = r3.as_dict()
        r1_dict['id'] = 1                                  # assign correct id vals
        r2_dict['id'] = 2
        r3_dict['id'] = 3
        r1_dict['pickup_time'] = 'Mon, 01 Jan 1 00:00:00 GMT'
        r2_dict['pickup_time'] = 'Mon, 01 Jan 1 00:00:00 GMT'
        r3_dict['pickup_time'] = 'Mon, 01 Jan 1 00:00:00 GMT'
        r1_dict['dropoff_time'] = 'Mon, 01 Jan 1 00:00:00 GMT'
        r2_dict['dropoff_time'] = 'Mon, 01 Jan 1 00:00:00 GMT'
        r3_dict['dropoff_time'] = 'Mon, 01 Jan 1 00:00:00 GMT'
        db.session.add(r1)
        db.session.add(r2)
        db.session.add(r3)
        db.session.commit()

        response = self.client.get('/rides/1')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.get_data()), {'ride': r1_dict})

        response = self.client.get('/rides/2')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.get_data()), {'ride': r2_dict})

        response = self.client.get('/rides/3')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.get_data()), {'ride': r3_dict})

    """
    test_add_ride
    -------------
    Tests that adding a new ride request works. Sends POST ride
    request data to '/rides/' and checks if the response json object
    is a valid ride request
    """
    @myvcr.use_cassette()
    @replace('steerclear.views.datetime', test_datetime(2015,6,13,1,2,3))
    def test_add_ride(self):
        self.maxDiff = None
        expected_pickup_time = datetime(2015,6,13,1,2,3) + timedelta(0, 10 * 60)
        expected_dropoff_time = expected_pickup_time + timedelta(0, 171)
        expected_pickup_string = expected_pickup_time.strftime('%a, %d %b %Y %H:%M:%S GMT')
        expected_dropoff_string = expected_dropoff_time.strftime('%a, %d %b %Y %H:%M:%S GMT')
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
        response = self.client.post('/rides', data=payload)
        payload[u'id'] = 1
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.get_data()), {u"ride": payload})

        bad_payload = payload.copy()
        bad_payload.pop('num_passengers', None)
        bad_payload.pop('id', None)
        r = self.client.post('/rides', data=bad_payload)
        self.assertEquals(r.status_code, 404)

        bad_payload = payload.copy()
        bad_payload.pop('start_latitude', None)
        bad_payload.pop('id', None)
        r = self.client.post('/rides', data=bad_payload)
        self.assertEquals(r.status_code, 404)

        bad_payload = payload.copy()
        bad_payload.pop('start_longitude', None)
        bad_payload.pop('id', None)
        r = self.client.post('/rides', data=bad_payload)
        self.assertEquals(r.status_code, 404)

        bad_payload = payload.copy()
        bad_payload.pop('end_latitude', None)
        bad_payload.pop('id', None)
        r = self.client.post('/rides', data=bad_payload)
        self.assertEquals(r.status_code, 404)

        bad_payload = payload.copy()
        bad_payload.pop('end_longitude', None)
        bad_payload.pop('id', None)
        r = self.client.post('/rides', data=bad_payload)
        self.assertEquals(r.status_code, 404)

    """
    test_rides_delete_bad_ride_id
    -----------------------------
    Test that api returns 404 to a ride id that doesn't exist
    """
    def test_rides_delete_bad_ride_id(self):
        # check that bad ride_id delete request returns 404
        response = self.client.delete('/rides/0')
        self.assertEquals(response.status_code, 404)

        dtime = datetime(1,1,1)
        db.session.add(Ride(1, (2.2, 3.3), (4.4, 5.5), dtime, 0, dtime))
        db.session.commit()

        # check that bad ride_id with not empty database returns 404
        response = self.client.delete('/rides/2')
        self.assertEquals(response.status_code, 404)

    """
    test_rides_delete_success
    -------------------------
    Tests that deleting a ride works
    """
    def test_rides_delete_success(self):
        dtime = datetime(1,1,1)
        r1 = Ride(1, (2.2, 3.3), (4.4, 5.5), dtime, 0, dtime) # add ride objects to db
        r2 = Ride(2, (3.3, 4.4), (5.5, 6.6), dtime, 0, dtime)
        r3 = Ride(3, (4.4, 5.5), (6.6, 7.7), dtime, 0, dtime)
        r2_dict = r2.as_dict()                             # store dict versions
        r3_dict = r3.as_dict()
        db.session.add(r1)
        db.session.add(r2)
        db.session.add(r3)
        db.session.commit()

        r2_dict['id'] = 2                                  # assign correct id vals
        r3_dict['id'] = 3

        # test can delete a ride
        response = self.client.delete('/rides/1')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(Ride.query.all()), 2)
        self.assertEquals(Ride.query.get(1), None)
        self.assertEquals(Ride.query.get(2).as_dict(), r2_dict)
        self.assertEquals(Ride.query.get(3).as_dict(), r3_dict)
        
        # test can delete a ride out of order
        response = self.client.delete('/rides/3')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(Ride.query.all()), 1)
        self.assertEquals(Ride.query.get(1), None)
        self.assertEquals(Ride.query.get(2).as_dict(), r2_dict)
        self.assertEquals(Ride.query.get(3), None)

        # test can delete final ride
        response = self.client.delete('/rides/2')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Ride.query.all(), [])
        self.assertEquals(Ride.query.get(1), None)
        self.assertEquals(Ride.query.get(2), None)
        self.assertEquals(Ride.query.get(3), None)

    @myvcr.use_cassette()
    @replace('steerclear.views.datetime', test_datetime(2015,6,13,1,2,3))
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
        db.session.add(Ride(1, (0.0, 0.0), (37.272042, -76.714027), None, None, datetime(2015,6,13,1,2,3)))
        db.session.commit()
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
        db.session.add(Ride(1, (0.0, 0.0), (0.0, 0.0), None, None, datetime(2015,6,13,1,2,3)))
        db.session.commit()
        pickup_loc = (37.273485, -76.719628)
        dropoff_loc = (37.280893, -76.719691)
        result = calculate_time_data(pickup_loc, dropoff_loc)
        self.assertEquals(result, None)    

    @myvcr.use_cassette()
    def test_calculate_time_delta_with_last_ride_bad_pickup_loc(self):
        db.session.add(Ride(1, (0.0, 0.0), (37.272042, -76.714027), None, None, datetime(2015,6,13,1,2,3)))
        db.session.commit()
        pickup_loc = (0.0, 0.0)
        dropoff_loc = (37.280893, -76.719691)
        result = calculate_time_data(pickup_loc, dropoff_loc)
        self.assertEquals(result, None)   

    @myvcr.use_cassette()
    def test_calculate_time_delta_with_last_ride_bad_dropoff_loc(self):
        db.session.add(Ride(1, (0.0, 0.0), (37.272042, -76.714027), None, None, datetime(2015,6,13,1,2,3)))
        db.session.commit()
        pickup_loc = (37.280893, -76.719691)
        dropoff_loc = (0.0, 0.0)
        result = calculate_time_data(pickup_loc, dropoff_loc)
        self.assertEquals(result, None)   

