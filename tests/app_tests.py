import steerclear
import unittest

class SteerClearTestCase(unittest.TestCase):
	def setUp(self):
		steerclear.app.config['TESTING'] = True
		self.app = steerclear.app.test_client()

	def test_heartbeat(self):
		response = self.app.get('/')
		self.assertEquals(response.status, "200 OK")
		self.assertEquals(response.data, "pulse")
