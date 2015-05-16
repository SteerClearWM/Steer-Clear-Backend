from steerclear import app, db
from steerclear.models import *
import unittest, tempfile, json

class SteerClearTestCase(unittest.TestCase):
	def setUp(self):
		_, db_abs_path = tempfile.mkstemp()
		app.config['TESTING'] = True
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
		self.client = app.test_client()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_heartbeat(self):
		response = self.client.get('/')
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.data, "pulse")

	def test_list_rides(self):
		response = self.client.get('/rides')
		self.assertEquals(response.status_code, 200)
		self.assertEquals(json.loads(response.data), {"rides": []})

