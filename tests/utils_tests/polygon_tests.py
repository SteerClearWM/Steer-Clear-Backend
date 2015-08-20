from steerclear.utils.polygon import SteerClearGISClient
import unittest
import os

cur_dirname = os.path.join(os.path.dirname(__file__), os.pardir)
shapefile_filename = cur_dirname + '/fixtures/shapefiles/campus_map/campus_map.shp'

class SteerClearGISClientTestCase(unittest.TestCase):

	def setUp(self):
		self.gis_client = SteerClearGISClient(shapefile_filename)

	def test_example(self):
		pass