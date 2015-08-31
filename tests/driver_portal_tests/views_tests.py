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
    tests that visiting '/' redirects to login page
    """
    def test_heartbeat(self):
        response = self.client.get('/')
        self.assertTemplateUsed('landing.html')

    """
    test_get_index_requires_login
    -----------------------------
    Tests that index page requires login
    """
    def test_get_index_requires_login(self):
        response = self.client.get(url_for('driver_portal.index'))
        self.assertEquals(response.status_code, 401)

    """
    test_get_index_admin_user
    --------------
    Tests that only logged in admin users can access the index page
    """
    def test_get_index_admin_user(self):
        self._login(self.admin_user)
        response = self.client.get(url_for('driver_portal.index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('index.html')

    """
    test_get_index_student_user
    ---------------------------
    Tests that logged in student users are redirected to the landing page
    """
    def test_get_index_student_user(self):
        self._login(self.student_user)
        response = self.client.get(url_for('driver_portal.index'))
        self.assertRedirects(response, url_for('driver_portal.heartbeat'))

