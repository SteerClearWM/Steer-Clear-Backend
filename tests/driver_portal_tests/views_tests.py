from steerclear import app, db
import unittest

"""
SteerClearTestCase
------------------
TestCase for driver side management
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
