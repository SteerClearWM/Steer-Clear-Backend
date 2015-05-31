from steerclear.eta import *
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

	def test_build_query(self):
		origins = (0.0,0.0)
		destinations = (0.0,0.0)
		query = build_query(origins, destinations)
		self.assertEquals(query, {
			'origins': '%f,%f' % origins, 
			'destinations': '%f,%f' % destinations
		})

	"""
	test_build_distancematrix_url
	-----------------------------
	Tests that build_distancematrix_url() correctly builds the google
	distancematrix api url given the start and end lat/long tuples
	"""
	def test_build_distancematrix_url(self):
		base_url = DISTANCEMATRIX_BASE_URL + '?'
		start = (0.0, 0.0)
		end = (0.0, 0.0)
		url = build_distancematrix_url(start, end)
		self.assertEquals(url, base_url + urllib.urlencode({
			'origins': "%f,%f" % start,
			'destinations': "%f,%f" % end
		}))

	"""
	test_calculate_eta
	------------------
	Tests that calculate_eta works as expected for a real request
	from Sadler to WM Hall. Uses response recorded in the cassette file
	"""
	@myvcr.use_cassette()
	def test_calculate_eta(self):
		start = (37.272042,-76.714027)
		end = (37.273485,-76.719628)
		eta = calculate_eta(start, end)
		self.assertEquals(eta, 252)

	"""
	test_calculate_eta_bad_status
	------------------
	Tests that calculate_eta returns None when the 'status' field
	is not 'OK'. Uses response recorded in the cassette file
	"""
	@myvcr.use_cassette()
	def test_calculate_eta_bad_status(self):
		start = (37.272042,-76.714027)
		end = (0,0)
		eta = calculate_eta(start, end)
		self.assertEquals(eta, None)

	"""
	test_calculate_eta_bad_rows
	---------------------------
	Tests that calculate_eta returns None when no 'rows' field
	is present in the response. Uses response recorded in the cassette file
	"""
	@myvcr.use_cassette()
	def test_calculate_eta_bad_rows(self):
		start = (0,0)
		end = (0,0)
		eta = calculate_eta(start, end)
		self.assertEquals(eta, None)

	"""
	test_calculate_eta_bad_elements
	-------------------------------
	Tests that calculate_eta returns None when no 'elements' field
	is present in the response. Uses response recorded in the cassette file
	"""
	@myvcr.use_cassette()
	def test_calculate_eta_bad_elements(self):
		start = (1,1)
		end = start
		eta = calculate_eta(start, end)
		self.assertEquals(eta, None)

	"""
	test_calculate_eta_bad_duration
	-------------------------------
	Tests that calculate_eta returns None when no 'duration' field
	is present in the response. Uses response recorded in the cassette file
	"""
	@myvcr.use_cassette()
	def test_calculate_eta_bad_duration(self):
		start = (2,2)
		end = start
		eta = calculate_eta(start, end)
		self.assertEquals(eta, None)

	"""
	test_calculate_eta_bad_value
	-------------------------------
	Tests that calculate_eta returns None when no 'value' field
	is present in the response. Uses response recorded in the cassette file
	"""
	@myvcr.use_cassette()
	def test_calculate_eta_bad_value(self):
		start = (3,3)
		end = start
		eta = calculate_eta(start, end)
		self.assertEquals(eta, None)
