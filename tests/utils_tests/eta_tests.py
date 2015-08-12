from steerclear.utils.eta import *
import unittest, urllib, vcr
from tests.base import base
from testfixtures import replace, test_datetime
from datetime import datetime, timedelta
from steerclear.api.views import calculate_time_data

# vcr object used to record api request responses or return already recorded responses
myvcr = vcr.VCR(cassette_library_dir='tests/fixtures/vcr_cassettes/eta_tests/')

"""
DMResponseTestCase
------------------
Test case for DMResponse class which
parses response objects from the google distancematrix api
"""
class DMResponseTestCase(unittest.TestCase):

    """
    setUp
    -----
    Set up some sample data for testing the eta functionality
    """
    def setUp(self):
        # an example of a correct response from the distance matrix api
        self.response = {
           "destination_addresses" : [
              "2006 Brooks Street, Williamsburg, VA 23185, USA",
              "1234 Richmond Road, Williamsburg, VA 23185, USA"
           ],
           "origin_addresses" : [
              "249 Stadium Drive, Williamsburg, VA 23186, USA",
              "2006 Brooks Street, Williamsburg, VA 23185, USA"
           ],
           "rows" : [
              {
                 "elements" : [
                    {
                       "distance" : {
                          "text" : "1.4 km",
                          "value" : 1436
                       },
                       "duration" : {
                          "text" : "4 mins",
                          "value" : 267
                       },
                       "status" : "OK"
                    },
                    {
                       "distance" : {
                          "text" : "1.4 km",
                          "value" : 1390
                       },
                       "duration" : {
                          "text" : "4 mins",
                          "value" : 238
                       },
                       "status" : "OK"
                    }
                 ]
              },
              {
                 "elements" : [
                    {
                       "distance" : {
                          "text" : "1 m",
                          "value" : 0
                       },
                       "duration" : {
                          "text" : "1 min",
                          "value" : 0
                       },
                       "status" : "OK"
                    },
                    {
                       "distance" : {
                          "text" : "1.4 km",
                          "value" : 1353
                       },
                       "duration" : {
                          "text" : "4 mins",
                          "value" : 239
                       },
                       "status" : "OK"
                    }
                 ]
              }
           ],
           "status" : "OK"
        }

        # another correct response
        self.response2 = {
           "destination_addresses" : [ "2006 Brooks Street, Williamsburg, VA 23185, USA" ],
           "origin_addresses" : [ "249 Stadium Drive, Williamsburg, VA 23186, USA" ],
           "rows" : [
              {
                 "elements" : [
                    {
                       "distance" : {
                          "text" : "1.4 km",
                          "value" : 1436
                       },
                       "duration" : {
                          "text" : "4 mins",
                          "value" : 267
                       },
                       "status" : "OK"
                    }
                 ]
              }
           ],
           "status" : "OK"
        }

        # represents an invalid request
        self.response3 = {
           "destination_addresses" : [],
           "origin_addresses" : [],
           "rows" : [],
           "status" : "INVALID_REQUEST"
        }

        # respresents a partialy bad request
        self.response4 = {
           "destination_addresses" : [ "37.273485,-76.719628", "37.280893,-76.719691" ],
           "origin_addresses" : [ "0,0", "2006 Brooks Street, Williamsburg, VA 23185, USA" ],
           "rows" : [
              {
                 "elements" : [
                    {
                       "status" : "ZERO_RESULTS"
                    },
                    {
                       "status" : "ZERO_RESULTS"
                    }
                 ]
              },
              {
                 "elements" : [
                    {
                       "distance" : {
                          "text" : "1 m",
                          "value" : 0
                       },
                       "duration" : {
                          "text" : "1 min",
                          "value" : 0
                       },
                       "status" : "OK"
                    },
                    {
                       "distance" : {
                          "text" : "1.4 km",
                          "value" : 1353
                       },
                       "duration" : {
                          "text" : "4 mins",
                          "value" : 239
                       },
                       "status" : "OK"
                    }
                 ]
              }
           ],
           "status" : "OK"
        }

    """
    test_dmresponse_invalid_request
    -------------------------------
    Tests that the dmresponse handles an
    invalid request correctly by settings its
    :data: attribute to None
    """
    def test_dmresponse_invalid_request(self):
        dmr = DMResponse(self.response3)
        self.assertEquals(dmr.data, None)

    """
    test_get_eta_no_response
    ------------------------
    Tests that dmresponse returns None
    if given a bad response json object
    """
    def test_get_eta_no_response(self):
        dmr = DMResponse(None)
        eta = dmr.get_eta()
        self.assertEquals(eta, None)

        dmr = DMResponse({})
        eta = dmr.get_eta()
        self.assertEquals(eta, None)

    """
    test_get_eta_no_rows
    --------------------
    Tests that dmresponse returns None if there is
    no 'rows' field in response oject
    """
    def test_get_eta_no_rows(self):
        # makes a copy of response and pops off 'row' field
        def make_test(response):
            bad_response = response.copy()
            bad_response.pop(u'rows')
            dmresponse = DMResponse(bad_response)
            eta = dmresponse.get_eta()
            self.assertEquals(eta, None)

        # test all types of responses
        make_test(self.response)
        make_test(self.response2)
        make_test(self.response3)
        make_test(self.response4)

    """
    test_get_eta_empty_rows
    --------------------
    Tests that dmresponse returns []] if 'rows' is empty
    """
    def test_get_eta_empty_rows(self):
        # make copy of response and sets 'row' field to []
        def make_test(response):
            bad_response = response.copy()
            bad_response[u'rows'] = []
            dmresponse = DMResponse(bad_response)
            eta = dmresponse.get_eta()
            self.assertEquals(eta, None)

        # test all types of responses
        make_test(self.response)
        make_test(self.response2)
        make_test(self.response3)
        make_test(self.response4)

    """
    test_get_eta_no_elements
    --------------------
    Tests that dmresponse returns None if there is
    no 'elements' field in response oject
    """
    def test_get_eta_no_elements(self):
        # checks that bad response return None for get_eta
        def make_test(bad_response):
            dmresponse = DMResponse(bad_response)
            eta = dmresponse.get_eta()
            self.assertEquals(eta, None)

        # test response
        bad_response = self.response.copy()
        bad_response[u'rows'][0].pop(u'elements')
        make_test(bad_response)

        # test response2
        bad_response = self.response2.copy()
        bad_response[u'rows'][0].pop(u'elements')
        make_test(bad_response)

        # test response3
        bad_response = self.response3.copy()
        dmresponse = DMResponse(bad_response)
        make_test(bad_response)

        # test response4
        bad_response = self.response4.copy()
        bad_response[u'rows'][0].pop(u'elements')
        dmresponse = DMResponse(bad_response)
        make_test(bad_response)

    """
    test_get_eta_empty_elements
    --------------------
    Tests that dmresponse returns []] if 'elements' is empty
    """
    def test_get_eta_empty_elements(self):
        # checks that bad response return None for get_eta
        def make_test(bad_response):
            dmresponse = DMResponse(bad_response)
            eta = dmresponse.get_eta()
            self.assertEquals(eta, None)

        # test response
        bad_response = self.response.copy()
        bad_response[u'rows'][0][u'elements'] = []
        make_test(bad_response)

        # test response2
        bad_response = self.response2.copy()
        bad_response[u'rows'][0][u'elements'] = []
        make_test(bad_response)

        # test response3
        bad_response = self.response3.copy()
        make_test(bad_response)

        # test response4
        bad_response = self.response4.copy()
        bad_response[u'rows'][0][u'elements'] = []
        make_test(bad_response)

    """
    test_get_eta_bad_element_status
    --------------------
    Tests that dmresponse returns None if the
    element status is a bad status
    """
    def test_get_eta_bad_element_status(self):
        # checks that bad response return None for get_eta
        def make_test(bad_response):
            dmresponse = DMResponse(bad_response)
            eta = dmresponse.get_eta()
            self.assertEquals(eta, None)

        # test response
        bad_response = self.response.copy()
        bad_response[u'rows'][0][u'elements'][0][u'status'] = u'BAD'
        make_test(bad_response)

        # test response2
        bad_response = self.response2.copy()
        bad_response[u'rows'][0][u'elements'][0][u'status'] = u'BAD'
        make_test(bad_response)

        # test response3
        bad_response = self.response3.copy()
        make_test(bad_response)

        # test response4
        bad_response = self.response4.copy()
        make_test(bad_response)

    """
    test_get_eta_no_duration
    --------------------
    Tests that dmresponse returns None if there is
    no 'duration' field in response oject
    """
    def test_get_eta_no_duration(self):
        # checks that bad response return None for get_eta
        def make_test(bad_response):
            dmresponse = DMResponse(bad_response)
            eta = dmresponse.get_eta()
            self.assertEquals(eta, None)

        # test response
        bad_response = self.response.copy()
        bad_response[u'rows'][0][u'elements'][0].pop(u'duration')
        make_test(bad_response)

        # test response2
        bad_response = self.response2.copy()
        bad_response[u'rows'][0][u'elements'][0].pop(u'duration')
        make_test(bad_response) 

        # test response3
        bad_response = self.response3.copy()
        make_test(bad_response)

        # test response4
        bad_response = self.response4.copy()
        make_test(bad_response)

    """
    test_get_eta_no_value
    --------------------
    Tests that dmresponse returns None if there is
    no 'value' field in response oject
    """
    def test_get_eta_no_value(self):
        # checks that bad response return None for get_eta
        def make_test(bad_response):
            dmresponse = DMResponse(bad_response)
            eta = dmresponse.get_eta()
            self.assertEquals(eta, None)

        # test response
        bad_response = self.response.copy()
        bad_response[u'rows'][0][u'elements'][0][u'duration'].pop(u'value')
        make_test(bad_response)

        # test response2
        bad_response = self.response2.copy()
        bad_response[u'rows'][0][u'elements'][0][u'duration'].pop(u'value')
        make_test(bad_response)

        # test response2
        bad_response = self.response2.copy()
        make_test(bad_response)

        # test response2
        bad_response = self.response2.copy()
        make_test(bad_response)

    """
    test_get_eta_success
    --------------------
    Tests that dmresponse correctly returns
    all eta values from a correct response object
    """
    def test_get_eta_success(self):
        # test response
        dmr = DMResponse(self.response)
        eta = dmr.get_eta()
        self.assertEquals(eta, [[267, 238], [0, 239]])

        # test response2
        dmr = DMResponse(self.response2)
        eta = dmr.get_eta()
        self.assertEquals(eta, [[267]])

        # test response3 - should return None
        dmr = DMResponse(self.response3)
        eta = dmr.get_eta()
        self.assertEquals(eta, None)

        # test response4 - should return None
        dmr = DMResponse(self.response4)
        eta = dmr.get_eta()
        self.assertEquals(eta, None)

    """
    test_get_addresses_no_response
    ------------------------
    Tests that dmresponse returns None
    if given a bad response json object
    """
    def test_get_addresses_no_response(self):
        dmr = DMResponse(None)
        addresses = dmr.get_addresses()
        self.assertEquals(addresses, None)

        dmr = DMResponse({})
        addresses = dmr.get_addresses()
        self.assertEquals(addresses, None)

    """
    test_get_addresses_no_origin_addresses
    --------------------
    Tests that dmresponse returns None if there is
    no 'origin_addresses' field in response oject
    """
    def test_get_addresses_no_origin_addresses(self):
        # pops 'origin_addresses' field off response and checks that
        # get_addresses returns None
        def make_test(response):
            bad_response = response.copy()
            bad_response.pop(u'origin_addresses')
            dmr = DMResponse(bad_response)
            addresses = dmr.get_addresses()
            self.assertEquals(addresses, None)        

        # test all responses
        make_test(self.response)
        make_test(self.response2)
        make_test(self.response3)
        make_test(self.response4)

    """
    test_get_addresses_empty_origin_addresses
    --------------------
    Tests that dmresponse returns None if there
    is no 'origin_addresses' field in the response
    """
    def test_get_addresses_empty_origin_addresses(self):
        # sets 'origin_addresses' field of response to be []
        # and checks that get_addresses returns None
        def make_test(response):
            bad_response = response.copy()
            bad_response[u'origin_addresses'] = []
            dmr = DMResponse(bad_response)
            addresses = dmr.get_addresses()
            self.assertEquals(addresses, None)

        # test all responses
        make_test(self.response)
        make_test(self.response2)
        make_test(self.response3)
        make_test(self.response4)

    """
    test_get_addresses_no_destination_addresses
    --------------------
    Tests that dmresponse returns None if there is
    no 'destination_addresses' field in response oject
    """
    def test_get_addresses_no_destination_addresses(self):
        # pops 'destination_addresses' field off response and checks that
        # get_addresses returns None
        def make_test(response):
            bad_response = response.copy()
            bad_response.pop(u'destination_addresses')
            dmr = DMResponse(bad_response)
            addresses = dmr.get_addresses()
            self.assertEquals(addresses, None)        

        # test all responses
        make_test(self.response)
        make_test(self.response2)
        make_test(self.response3)
        make_test(self.response4)

    """
    test_get_addresses_empty_destination_addresses
    --------------------
    Tests that dmresponse returns None if there
    is no 'destination_addresses' field in the response
    """
    def test_get_addresses_empty_destination_addresses(self):
        # sets 'destination_addresses' field of response to be []
        # and checks that get_addresses returns None
        def make_test(response):
            bad_response = response.copy()
            bad_response[u'destination_addresses'] = []
            dmr = DMResponse(bad_response)
            addresses = dmr.get_addresses()
            self.assertEquals(addresses, None)

        # test all responses
        make_test(self.response)
        make_test(self.response2)
        make_test(self.response3)
        make_test(self.response4)

    """
    test_get_addresses
    ------------------
    Tests that dmresponse will get the addresses
    correctly for a response object
    """
    def test_get_addresses(self):
        # test response
        dmr = DMResponse(self.response)
        addresses = dmr.get_addresses()
        expected_addresses = (
            self.response[u'origin_addresses'],
            self.response[u'destination_addresses']
        )
        self.assertEquals(addresses, expected_addresses)

        # test response2
        dmr = DMResponse(self.response2)
        addresses = dmr.get_addresses()
        expected_addresses = (
            self.response2[u'origin_addresses'],
            self.response2[u'destination_addresses']
        )
        self.assertEquals(addresses, expected_addresses)

        # test response3 - should return None
        dmr = DMResponse(self.response3)
        addresses = dmr.get_addresses()
        self.assertEquals(addresses, None)

        # test response4
        dmr = DMResponse(self.response4)
        addresses = dmr.get_addresses()
        expected_addresses = (
            self.response4[u'origin_addresses'],
            self.response4[u'destination_addresses']
        )
        self.assertEquals(addresses, expected_addresses)


class SteerClearDMClientTestCase(unittest.TestCase):

    def setUp(self):
        self.dmclient = SteerClearDMClient()

    """
    test_format_query
    ----------------
    Tests that _format_query will take a list of origin lat/long pairs
    and a list of destinations lat/long pairs and build the right
    google distancematrix api query string
    """
    def test_format_query(self):
        # Test that query in formated correclty zero lat/long position
        origins = [(0.0,0.0)]
        destinations = [(0.0,0.0)]
        query = self.dmclient._format_query(origins, destinations)
        self.assertEquals(query, {
            'origins': '%f,%f' % origins[0], 
            'destinations': '%f,%f' % destinations[0]
        })

        origins = [(-71,70), (65,45.2345)]
        destinations = [(65,45.2345), (-71,70)]
        query = self.dmclient._format_query(origins, destinations)
        self.assertEquals(query, {
            'origins': ('%f,%f' % origins[0]) + '|' + ('%f,%f' % origins[1]), 
            'destinations': ('%f,%f' % destinations[0]) + '|' + ('%f,%f' % destinations[1])
        })

    """
    test_build_url
    -----------------------------
    Tests that _build_url() correctly builds the google
    distancematrix api url given a query string
    """
    def test_build_url(self):
        base_url = DISTANCEMATRIX_BASE_URL + '?'

        # build query string and url
        origins = [(0.0, 0.0)]
        destinations = [(0.0, 0.0)]
        query = self.dmclient._format_query(origins, destinations)
        url = self.dmclient._build_url(query)
        
        # this is the expected url
        expected_url = base_url + urllib.urlencode({
          'origins': "%f,%f" % origins[0],
          'destinations': "%f,%f" % destinations[0]
        })

        self.assertEquals(url, expected_url)

        # build query string and url
        origins = [(-71,70), (65,45.2345)]
        destinations = [(65,45.2345), (-71,70)]
        query = self.dmclient._format_query(origins, destinations)
        url = self.dmclient._build_url(query)

        # this is the expected url
        expected_url = base_url + urllib.urlencode({
            'origins': ('%f,%f' % origins[0]) + '|' + ('%f,%f' % origins[1]), 
            'destinations': ('%f,%f' % destinations[0]) + '|' + ('%f,%f' % destinations[1])
        })

        self.assertEquals(url, expected_url)

    """
    test_query_api_bad_origin_latlong
    ---------------------------------
    Tests that dmrclient handles no origin point correctly
    """
    @myvcr.use_cassette()
    def test_query_api_bad_origin_latlong(self):
        origins = []
        destinations = [(0.0, 0.0)]
        response = self.dmclient.query_api(origins, destinations)
        self.assertEquals(response, DMResponse(None))

    """
    test_query_api_bad_destination_latlong
    ---------------------------------
    Tests that dmrclient handles no destination point correctly
    """
    @myvcr.use_cassette()
    def test_query_api_bad_destination_latlong(self):
        origins = [(0.0, 0.0)]
        destinations = []
        response = self.dmclient.query_api(origins, destinations)
        self.assertEquals(response, DMResponse(None))

    """
    test_query_api_zero_coordinate
    ------------------------------
    Tests that dmrclient does not fail for weird lat/long coordinates
    """
    @myvcr.use_cassette()
    def test_query_api_zero_coordinate(self):
        origins = [(0.0, 0.0)]
        destinations = [(0.0, 0.0)]
        response = self.dmclient.query_api(origins, destinations)
        self.assertNotEquals(response, DMResponse(None))

    """
    test_query_api_single_origin
    ----------------------------
    Tests that dmclient does not fail for a normal query with
    a single origin and destination
    """
    @myvcr.use_cassette()
    def test_query_api_single_origin(self):
        # expected value [[238]]
        origins = [(37.272042, -76.714027)]
        destinations = [(37.280893, -76.719691)]
        response = self.dmclient.query_api(origins, destinations)
        self.assertNotEquals(response, DMResponse(None))
        self.assertEquals(response.get_eta(), [[238]])

    """
    test_query_api_multiple_origins
    ----------------------------
    Tests that dmclient does not fail for a normal query with
    a multiple origins and destinations
    """
    @myvcr.use_cassette()
    def test_query_api_multiple_origins(self):
        # expected value [[267, 238], [0, 239]]
        origins = [(37.272042, -76.714027), (37.273485, -76.719628)]
        destinations = [(37.273485, -76.719628), (37.280893, -76.719691)]
        response = self.dmclient.query_api(origins, destinations)
        self.assertEquals(response.get_eta(), [[267, 238], [0, 239]])
