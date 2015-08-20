from steerclear.utils.polygon import SteerClearGISClient
import unittest
import os

cur_dirname = os.path.join(os.path.dirname(__file__), os.pardir)
shapefile_filename = cur_dirname + '/fixtures/shapefiles/campus_map/campus_map.shp'

"""
SteerClearGISClientTestCase
---------------------------
Test case for testing SteerClearGISClient.
Makes sure that SteerClearGISClient can accurately
classify lat/long pairs as oncampus or off campus
"""
class SteerClearGISClientTestCase(unittest.TestCase):

    def setUp(self):
        self.gis_client = SteerClearGISClient(shapefile_filename)

    def test_is_on_campus_point_is_on_campus(self):
        # test with lat/long of william and mary
        result = self.gis_client.is_on_campus((37.272433, -76.716922))
        self.assertTrue(result)