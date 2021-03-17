#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is offices test
"""

# import de module unittest2 that we need to create test
import json
import unittest2 as unittest
from api.utils.test_base import BaseTestCase


class TestOffice(BaseTestCase):
	""" This is 'TestOffice' class to hold all our tests. Import our base test class. """

	def setUp(self):
		""" This method set up the test client. """
		super(TestOffice, self).setUp()

		self.office1 = {'officeCode': 'OF1', 'city': 'New Orleans', 'phone': '111', 'addressLine1': 'Bronx', 'addressLine2': 'New', 'state': 'NY', 'country': 'usa', 'postalCode': '889000', 'territory': 'NA'}


	def test_create_office(self):
		""" Test to create a new office with correct fields, using POST office endpoint. """

		response = self.client.post('/offices/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.office1))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(201, response.status_code)


	def test_create_offices_same_officeCode(self):
		""" Test to try to create a new office with an existing 'officeCode'; which is key field, using POST office endpoint. """

		response = self.client.post('/offices/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.office1))
		office = {'officeCode': 'OF1', 'city': 'Miami', 'phone': '555', 'addressLine1': 'Beach', 'addressLine2': '91', 'state': 'FL', 'country': 'usa', 'postalCode': '889000', 'territory': 'NA'}
		response = self.client.post('/offices/', headers={'Content-Type': 'application/json'}, data=json.dumps(office))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(422, response.status_code)


	def test_create_offices_with_empty_request(self):
		""" Test try to create a new office without data; using POST office endpoint. """

		office = {}
		response = self.client.post('/offices/', headers={'Content-Type': 'application/json'}, data=json.dumps(office))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(400, response.status_code)


	def test_create_offices_with_no_officeCode(self):
		""" Test try to create a new office without 'officeCode'; which is key data, using POST office endpoint. """

		office = {'city': 'Rochester', 'phone': '222', 'addressLine1': 'Bronx', 'addressLine2': 'Tampa', 'state': 'NY', 'country': 'usa', 'postalCode': '889000', 'territory': 'NA'}
		response = self.client.post('/offices/', headers={'Content-Type': 'application/json'}, data=json.dumps(office))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(400, response.status_code)


	def test_delete_specific_office(self):
		""" Test to get only one demanded office, using GET office by 'officeCode' endpoint. """

		response = self.client.post('/offices/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.office1))
		data = json.loads(response.data)
		print(data)
		response = self.client.delete('/offices/OF1', content_type='application/json')
		self.assertEqual(204, response.status_code)


	def test_get_office_details(self):
		""" Test to get only one demanded office, using GET office by 'officeCode' endpoint. """

		response = self.client.post('/offices/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.office1))
		response = self.client.get('/offices/OF1', content_type='application/json')
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


	def test_get_offices(self):
		""" Test to get all offices, using GET all endpoint. """

		response = self.client.post('/offices/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.office1))
		response = self.client.get('/offices/', content_type='application/json')
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


	def test_update_office(self):
		""" Test to update some details in only one office, using PUT office by 'officeCode' endpoint. """

		response = self.client.post('/offices/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.office1))
		office = {'officeCode': 'OF1', 'city': 'Miami', 'phone': '222', 'addressLine1': 'Bronx', 'addressLine2': 'New', 'state': 'NY', 'country': 'usa', 'postalCode': '889000', 'territory': 'NA'}
		response = self.client.put('/offices/OF1', headers={'Content-Type': 'application/json'}, data=json.dumps(office))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


	def test_update_office_details(self):
		""" Test to update some details in only one office, using PATCH office by 'officeCode' endpoint. """

		response = self.client.post('/offices/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.office1))
		office = {'officeCode': 'OF1', 'phone': '222', 'addressLine1': 'Bronx', 'addressLine2': 'New', 'postalCode': '889000'}
		response = self.client.patch('/offices/OF1', headers={'Content-Type': 'application/json'}, data=json.dumps(office))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


	# def tearDown(self)
# ...
if __name__ == "__main__":
	unittest.main()			#verbosity=2