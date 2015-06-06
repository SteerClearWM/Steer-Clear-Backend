from steerclear import app, db
from steerclear.models import *
import unittest, json
from datetime import datetime

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
    def test_add_ride(self):
        payload = {
                    u"num_passengers": 3,
                    u"start_latitude": 1.1,
                    u"start_longitude": 2.2,
                    u"end_latitude": 3.3,
                    u"end_longitude": 4.4,
                    u"pickup_time": u'Mon, 01 Jan 1 00:00:00 GMT',
                    u"travel_time": 0,
                    u"dropoff_time": u'Mon, 01 Jan 1 00:00:00 GMT',
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
