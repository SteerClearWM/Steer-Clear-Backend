from steerclear.api.eta import *
from steerclear.models import Ride
import unittest, json, urllib, vcr, requests, os

# vcr object used to record api request responses or return already recorded responses
myvcr = vcr.VCR(cassette_library_dir='tests/fixtures/vcr_cassettes/eta_tests/')

"""
ETATestCase
------------------
TestCase for testing all travel time caclulation module
using google's distancematrix api
"""
class ETATestCase(unittest.TestCase):
    
    """
    setUp
    -----
    Set up some sample data for testing the eta functionality
    """
    def setUp(self):
        self.element1 = {u'status': u'OK', u'duration': {u'value': 0}}
        self.element2 = {u'status': u'OK', u'duration': {u'value': 100}}
        self.elements1 = [self.element1]
        self.elements2 = [self.element2]
        self.elements = [self.element1, self.element2]
        self.row1 = {u'elements': self.elements1}
        self.row2 = {u'elements': self.elements2}
        self.row = {u'elements': self.elements}
        self.rows1 = [self.row1]
        self.rows2 = [self.row2]
        self.rows3 = [self.row1, self.row2]
        self.rows = [self.row1, self.row2, self.row]

    """
    test_build_url
    --------------
    Test that build_url() correctly appends the query dictionary
    to the base url for google distancematrix api
    """
    def test_build_url(self):
        base_url = DISTANCEMATRIX_BASE_URL + '?'
        query = {}
        url = build_url(query)
        self.assertEquals(url, base_url + urllib.urlencode(query))

        query = {'test': 'hello,world'}
        url = build_url(query)
        self.assertEquals(url, base_url + urllib.urlencode(query))

        query = {'origins': '-71,70', 'destinations': '65,45.2345'}
        url = build_url(query)
        self.assertEquals(url, base_url + urllib.urlencode(query))

        query = {'origins': '-71,70|65,45.2345', 'destinations': '65,45.2345|-71,70'}
        url = build_url(query)
        self.assertEquals(url, base_url + urllib.urlencode(query))

    """
    test_build_query
    ----------------
    Tests that build_query will take a list of origin lat/long pairs
    and a list of destinations lat/long pairs and build the right
    google distancematrix api url
    """
    def test_build_query(self):
        origins = [(0.0,0.0)]
        destinations = [(0.0,0.0)]
        query = build_query(origins, destinations)
        self.assertEquals(query, {
            'origins': '%f,%f' % origins[0], 
            'destinations': '%f,%f' % destinations[0]
        })

        origins = [(-71,70), (65,45.2345)]
        destinations = [(65,45.2345), (-71,70)]
        query = build_query(origins, destinations)
        self.assertEquals(query, {
            'origins': ('%f,%f' % origins[0]) + '|' + ('%f,%f' % origins[1]), 
            'destinations': ('%f,%f' % destinations[0]) + '|' + ('%f,%f' % destinations[1])
        })

    """
    test_build_distancematrix_url
    -----------------------------
    Tests that build_distancematrix_url() correctly builds the google
    distancematrix api url given the start and end lat/long tuples
    """
    def test_build_distancematrix_url(self):
        base_url = DISTANCEMATRIX_BASE_URL + '?'
        origins = [(0.0, 0.0)]
        destinations = [(0.0, 0.0)]
        url = build_distancematrix_url(origins, destinations)
        self.assertEquals(url, base_url + urllib.urlencode({
          'origins': "%f,%f" % origins[0],
          'destinations': "%f,%f" % destinations[0]
        }))

        origins = [(-71,70), (65,45.2345)]
        destinations = [(65,45.2345), (-71,70)]
        url = build_distancematrix_url(origins, destinations)
        query = {
            'origins': ('%f,%f' % origins[0]) + '|' + ('%f,%f' % origins[1]), 
            'destinations': ('%f,%f' % destinations[0]) + '|' + ('%f,%f' % destinations[1])
        }
        self.assertEquals(url, base_url + urllib.urlencode(query))

    """
    test_get_element_eta
    --------------------
    Tests that get_element_eta will corectly get the eta from an
    element field
    """
    def test_get_element_eta(self):
        def make_test(element, result):
            eta = get_element_eta(element)
            self.assertEquals(eta, result)
        make_test(None, None)
        make_test({}, None)
        make_test({u'status': u'Not Found'}, None)
        make_test({u'status': u'OK'}, None)
        make_test({u'status': u'OK', u'duration': {}}, None)
        make_test(self.element1, 0)
        make_test(self.element2, 100)

    """
    test_get_elements_eta
    ---------------------
    Tests that get_elements_eta will corectly get all eta's from
    an elements field
    """
    def test_get_elements_eta(self):
        def make_test(elements, result):
            eta_list = get_elements_eta(elements)
            self.assertEquals(eta_list, result)
        make_test(None, None)
        make_test([], None)
        make_test([self.element1, None], None)
        make_test([self.element2, None], None)
        make_test(self.elements1, [0])
        make_test(self.elements2, [100])
        make_test(self.elements, [0, 100])

    """
    test_get_row_eta
    ----------------
    Tests that get_row_eta will get the eta_list
    from a row field
    """
    def test_get_row_eta(self):
        def make_test(row, result):
            eta_list = get_row_eta(row)
            self.assertEquals(eta_list, result)
        make_test(None, None)
        make_test({}, None)
        make_test(self.row1, [0])
        make_test(self.row2, [100])
        make_test(self.row, [0, 100])

    """
    test_get_rows_eta
    -----------------
    Tests that get_rows_eta will get all eta_lists from
    the rows field
    """
    def test_get_rows_eta(self):
        def make_test(rows, num_queries, result):
            eta_list = get_rows_eta(rows, num_queries)
            self.assertEquals(eta_list, result)
        make_test(None, 1, None)
        make_test([], 1, None)
        make_test([], 0, None)
        make_test(self.rows1, 3, None)
        make_test([self.row1, None], 2, None)
        make_test(self.rows1, 1, [[0]])
        make_test(self.rows2, 1, [[100]])
        make_test(self.rows3, 2, [[0], [100]])
        make_test(self.rows, 3, [[0], [100], [0, 100]])

    """
    test_time_between_locations
    -----------------------
    Tests that time_between_rides will return the right
    pickup_time_sec and travel_time_sec given two ride requests
    """
    @myvcr.use_cassette()
    def test_time_between_locations(self):
        origins = [(37.272042, -76.714027), (37.273485, -76.719628)]
        destinations = [(37.273485, -76.719628), (37.280893, -76.719691)]
        eta = time_between_locations(origins, destinations)
        self.assertEquals(eta, [[252, 218], [0, 171]])

    """
    test_time_between_locations_bad_latlong
    -----------------------------------
    Tests that time_between_rides will return None
    given a bad lat/long field for one of the ride requests
    """
    @myvcr.use_cassette()
    def test_time_between_locations_bad_latlong(self):
        origins = [(0.0, 0.0), (37.273485, -76.719628)]
        destinations = [(37.273485, -76.719628), (37.280893, -76.719691)]
        eta = time_between_locations(origins, destinations)
        self.assertEquals(eta, None)

    @myvcr.use_cassette()
    def test_time_between_locations_no_start_loc(self):
        origins = [(37.273485, -76.719628)]
        destinations = [(37.280893, -76.719691)]
        eta = time_between_locations(origins, destinations)
        self.assertEquals(eta, [[171]])
