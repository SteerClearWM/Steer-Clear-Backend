from steerclear import app, db
from steerclear.models import *
import unittest, json

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
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
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
    def test_list_rides(self):
        response = self.client.get('/rides')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.get_data()), {"rides": []})

    """
    test_add_ride
    -------------
    Tests that adding a new ride request works. Sends POST ride
    request data to '/rides/' and checks if the response json object
    is a valid ride request
    """
    def test_add_ride(self):
        payload = {
                    u"phone_number": u"123-456-7890",
                    u"num_passengers": 3,
                    u"start_latitude": 1.1,
                    u"start_longitude": 2.2,
                    u"end_latitude": 3.3,
                    u"end_longitude": 4.4,
                  }
        response = self.client.post('/rides', data=payload)
        payload[u'id'] = 1
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.get_data()), {u"ride": payload})
