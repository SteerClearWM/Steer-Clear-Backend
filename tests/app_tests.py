import app
import unittest

class SteerClearTestCase(unittest.TestCase):
	def setUp(self):
		app.app.config['TESTING'] = True
		self.app = app.app.test_client()

	def test_heartbeat(self):
		response = self.app.get('/')
		self.assertEquals(response.status, "200 OK")
		self.assertEquals(response.data, "pulse")
