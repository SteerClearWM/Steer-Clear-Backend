from steerclear.eta import *
import unittest, json, urllib

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