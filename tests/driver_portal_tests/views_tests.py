from steerclear import app, db
from steerclear.models import User
from flask import url_for
from tests.base import base

"""
SteerClearTestCase
------------------
TestCase for driver side management
"""
class SteerClearTestCase(base.SteerClearBaseTestCase):

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
    test_get_index_requires_login
    -----------------------------
    Tests that index page requires login
    """
    def test_get_index_requires_login(self):
        response = self.client.get(url_for('driver_portal.index'))
        self.assertEquals(response.status_code, 401)

    """
    test_get_index
    --------------
    Tests that only logged in users can access the index page
    """
    def test_get_index(self):
        user = self._create_user()
        self._login(user)
        response = self.client.get(url_for('driver_portal.index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('index.html')

