from steerclear.eta import *
import unittest, json, urllib, vcr, requests, os

dirname = os.path.dirname(os.path.abspath(__file__))

myvcr = vcr.VCR(cassette_library_dir='tests/fixtures/vcr_cassettes/eta_tests/')

"""
ETATestCase
------------------
TestCase for testing all travel time caclulation module
using google's distancematrix api
"""
class ETATestCase(unittest.TestCase):
	
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

	def test_build_distancematrix_url(self):
		base_url = DISTANCEMATRIX_BASE_URL + '?'
		start = (0.0, 0.0)
		end = (0.0, 0.0)
		url = build_distancematrix_url(start, end)
		self.assertEquals(url, base_url + urllib.urlencode({
			'origins': "%f,%f" % start,
			'destinations': "%f,%f" % end
		}))

	@myvcr.use_cassette()
	def test_calculate_eta(self):
		start = (37.272042,-76.714027)
		end = (37.273485,-76.719628)
		eta = calculate_eta(start, end)
		self.assertEquals(eta, 252)

	@myvcr.use_cassette()
	def test_calculate_eta_bad_status(self):
		start = (37.272042,-76.714027)
		end = (0,0)
		eta = calculate_eta(start, end)
		self.assertEquals(eta, None)
