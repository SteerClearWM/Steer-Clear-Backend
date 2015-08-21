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

    def test_is_on_campus_points_in_center_of_campus(self):
        # test with lat/long of william and mary
        result = self.gis_client.is_on_campus((37.272433, -76.716922))
        self.assertTrue(result)

        # test with lat/long of sadler center
        result = self.gis_client.is_on_campus((37.271819, -76.714061))

    def test_is_on_campus_points_near_perimeter_of_campus(self):
        # test point near barret hall
        result = self.gis_client.is_on_campus((37.269028, -76.711410))
        self.assertTrue(result)

        # test point near jefferson hall
        result = self.gis_client.is_on_campus((37.269501, -76.710186))
        self.assertTrue(result)

        # test point near colonial williamsburg but still on campus
        result = self.gis_client.is_on_campus((37.270837, -76.707575))
        self.assertTrue(result)

        # test point near blow hall
        result = self.gis_client.is_on_campus((37.272114, -76.709993))
        self.assertTrue(result)

        # test point near bryan hall
        result = self.gis_client.is_on_campus((37.272938, -76.712275))
        self.assertTrue(result)

        # test point near zable hall
        result = self.gis_client.is_on_campus((37.273959, -76.713427))
        self.assertTrue(result)

        # test point near frat castles
        result = self.gis_client.is_on_campus((37.274754, -76.718091))
        self.assertTrue(result)

        # test point near rec center
        result = self.gis_client.is_on_campus((37.274705, -76.720931))
        self.assertTrue(result)

        # test point near randolph complex
        result = self.gis_client.is_on_campus((37.270857, -76.719126))
        self.assertTrue(result)

        # test point near jamestown south
        result = self.gis_client.is_on_campus((37.268358, -76.712992))
        self.assertTrue(result)

        # test point near PBK
        result = self.gis_client.is_on_campus((37.267523, -76.714738))
        self.assertTrue(result)

        # test point near business school
        result = self.gis_client.is_on_campus((37.266099, -76.717825))
        self.assertTrue(result)
