#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is offices test
"""

# import de module unittest2 that we need to create test
from api.models.offices import Office
from api.utils.test_base import BaseTestCase
import unittest2 as unittest
import json


def create_offices():
	""" This is 'create_offices' method to create offices using the SQLAlchemy model to facilitate testing. """

	office1 = Office(officeCode="OFnba", city="New York", phone="555-444-777", addressLine1="Central Park", addressLine2="London", state="NY", country="usa", postalCode="889000", territory="NA").create()


class TestOffice(BaseTestCase):
	""" This is 'TestOffice' class to hold all our tests. Import our base test class. """

	def setUp(self):
		""" This method set up the test client and call create_offices() method to create the offices. """
		super(TestOffice, self).setUp()
		create_offices()

	def test_create_offices(self):
		""" Test to create a new office with correct fields, using POST office endpoint. """

		office = {"officeCode": "OFnba", "city": "New York", "phone": "555-444-777", "addressLine1": "Central Park", "addressLine2": "London", "state": "NY", "country": "usa", "postalCode": "889000", "territory": "NA"}

		response = self.app.post('/offices/', data=json.dumps(office), content_type='application/json')
		data = json.loads(response.data)
		self.assertEqual(201, response.status_code)
		self.assertTrue('officeCode' in data)
		self.assertTrue('city' in data)
		self.assertTrue('phone' in data)
		self.assertTrue('addressLine1' in data)
		self.assertTrue('country' in data)
		self.assertTrue('postalCode' in data)
		self.assertTrue('territory' in data)

	def test_create_offices_no_officeCode(self):
		""" Test try to create a new office without officeCode key field, using POST office endpoint. """

		office = {"city": "New York", "phone": "555-444-777", "addressLine1": "Central Park", "addressLine2": "London", "state": "NY", "country": "usa", "postalCode": "889000", "territory": "NA"}

		response = self.app.post('/offices/', data=json.dumps(office), content_type='application/json')
		data = json.loads(response.data)
		self.assertEqual(422, response.status_code)

	def test_create_offices_same_officeCode(self):
		""" Test try to create a new office with an already existent 'officeCode'; which is key field, using POST office endpoint. """

		office = {"officeCode": "OFnba", "city": "Miami Beach", "phone": "333-444-777", "addressLine1": "89", "addressLine2": "4", "state": "MA", "country": "usa", "postalCode": "779000", "territory": "NA"}

		response = self.app.post('/offices/', data=json.dumps(office), content_type='application/json')
		data = json.loads(response.data)
		self.assertEqual(400, response.status_code)

	def test_create_offices_same_phone(self):
		""" Test try to create a new office with an already existent 'phone'; which should be unique, using POST office endpoint. """

		office = {"officeCode": "OFnbc", "city": "Miami Beach", "phone": "555-444-777", "addressLine1": "89", "addressLine2": "4", "state": "MA", "country": "usa", "postalCode": "779000", "territory": "NA"}

		response = self.app.post('/offices/', data=json.dumps(office), content_type='application/json')
		data = json.loads(response.data)
		self.assertEqual(400, response.status_code)

	def test_get_offices(self):
		""" Test to get all offices, using GET all endpoint. """

		response = self.app.get('/offices/', content_type='application/json')
		data = json.loads(response.data)
		self.assertEqual(200, response.status_code)
		self.assertTrue('offices' in data)

	def test_get_office_details(self):
		""" Test to get only one demanded office, using GET office by 'officeCode' endpoint. """

		response = self.app.get('/offices/OFnba', content_type='application/json')
		data = json.loads(response.data)
		self.assertEqual(200, response.status_code)
		self.assertTrue('office' in data)

	def test_update_office_details(self):
		""" Test to update some details in only one office, using PUT office by 'officeCode' endpoint. """

		office = {"officeCode": "OFnba", "city": "Miami Beach", "phone": "000-444-777", "addressLine1": "5ta Avenue", "country": "usa", "postalCode": "159000", "territory": "SUR"}

		response = self.app.put('/offices/OFnba', data=json.dumps(office), content_type='application/json')
		self.assertEqual(200, response.status_code)

	def test_update_office_field(self):
		""" Test to update only one office field, using PATCH office by 'officeCode' endpoint. """

		office = {"territory": "NOR"}
		response = self.app.patch('/offices/OFnba', data=json.dumps(office), content_type='application/json')
		self.assertEqual(200, response.status_code)

	def test_delete_office(self):
		""" Test to DELETE only one office, using DELETE office endpoint. """

		response = self.app.delete('/offices/OFnba')
		self.assertEqual(204, response.status_code)


# ...
if __name__ == "__main__":
	unittest.main(verbosity=2)