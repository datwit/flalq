#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is offices test
"""

# import de module unittest2 that we need to create test
import json
import unittest2 as unittest
from api.utils.test_base import BaseTestCase
from api.models.offices import Office
from api.utils.database import session


def create_offices():
	""" This is 'create_offices' method to create offices using the SQLAlchemy model to facilitate testing. """

	office1 = Office(officeCode="OF1", city="New York", phone="111", addressLine1="Central Park", addressLine2="London", state="NY", country="usa", postalCode="889000", territory="NA")
	try:
		session.add(office1)
		session.commit()
	except Exception as e:
		session.rollback()


class TestOffice(BaseTestCase):
	""" This is 'TestOffice' class to hold all our tests. Import our base test class. """

	def setUp(self):
		""" This method set up the test client and call create_offices() method to create the offices. """
		super(TestOffice, self).setUp()
		create_offices()

	def test_create_office(self):
		""" Test to create a new office with correct fields, using POST office endpoint. """

		office = {'officeCode': 'OF2', 'city': 'New Orleans', 'phone': '222', 'addressLine1': 'Bronx', 'addressLine2': 'New', 'state': 'NY', 'country': 'usa', 'postalCode': '889000', 'territory': 'NA'}
		response = self.client().post('/offices/', headers={'Content-Type': 'application/json'}, data=json.dumps(office))
		data = json.loads(response.data)
		self.assertEqual(201, response.status_code)
		# self.assertTrue(data.get('officeCode'))

	def test_create_offices_same_officeCode(self):
		""" Test to try to create a new office with an existing 'officeCode'; which is key field, using POST office endpoint. """

		office = {'officeCode': 'OF2', 'city': 'Miami Beach', 'phone': '222', 'addressLine1': 'Bronx', 'addressLine2': 'Misisipi', 'state': 'NY', 'country': 'usa', 'postalCode': '889000', 'territory': 'NA'}
		response = self.client().post('/offices/', headers={'Content-Type': 'application/json'}, data=json.dumps(office))
		data = json.loads(response.data)
		self.assertEqual(400, response.status_code)
    #     self.assertTrue(data.get('error'))

	def test_create_offices_same_phone(self):
		""" Test try to create a new office with an existing 'phone'; which should be unique, using POST office endpoint. """

		office = {'officeCode': 'OF3', 'city': 'Rochester', 'phone': '222', 'addressLine1': 'Bronx', 'addressLine2': 'Misisipi', 'state': 'NY', 'country': 'usa', 'postalCode': '889000', 'territory': 'NA'}
		response = self.client().post('/offices/', headers={'Content-Type': 'application/json'}, data=json.dumps(office))
		data = json.loads(response.data)
		self.assertEqual(400, response.status_code)
	# 	self.assertTrue(data.get('error'))

	def test_create_offices_with_no_officeCode(self):
		""" Test try to create a new office without 'officeCode'; which is key data, using POST office endpoint. """

		office = {'city': 'Rochester', 'phone': '222', 'addressLine1': 'Bronx', 'addressLine2': 'Misisipi', 'state': 'NY', 'country': 'usa', 'postalCode': '889000', 'territory': 'NA'}
		response = self.client().post('/offices/', headers={'Content-Type': 'application/json'}, data=json.dumps(office))
		data = json.loads(response.data)
		self.assertEqual(400, response.status_code)
		# self.assertFalse(data.get('officeCode'))

	def test_create_offices_with_empty_request(self):
		""" Test try to create a new office without data; using POST office endpoint. """

		office = {}
		response = self.client().post('/offices/', headers={'Content-Type': 'application/json'}, data=json.dumps(office))
		data = json.loads(response.data)
		self.assertEqual(400, response.status_code)

	def test_get_offices(self):
		""" Test to get all offices, using GET all endpoint. """

		response = self.client().get('/offices/', content_type='application/json')
		data = json.loads(response.data)
		self.assertEqual(200, response.status_code)

	def test_get_office_details(self):
		""" Test to get only one demanded office, using GET office by 'officeCode' endpoint. """

		response = self.client().get('/offices/OF1', content_type='application/json')
		data = json.loads(response.data)
		self.assertEqual(200, response.status_code)
		# self.assertTrue(data.get('officeCode'))

	def test_update_office_details(self):
		""" Test to update some details in only one office, using PUT office by 'officeCode' endpoint. """

		office = {'officeCode': 'OF1', 'city': 'Toronto', 'phone': '333', 'addressLine1': 'Bronx', 'addressLine2': 'Florida', 'state': 'NY', 'country': 'usa', 'postalCode': '889000', 'territory': 'NA'}
		response = self.client().put('/offices/OF1', headers={'Content-Type': 'application/json'}, data=json.dumps(office))
		self.assertEqual(201, response.status_code)

	def test_delete_specific_office(self):
		""" Test to get only one demanded office, using GET office by 'officeCode' endpoint. """

		response = self.client().delete('/offices/OF1', content_type='application/json')
		self.assertEqual(204, response.status_code)

	# # "PATCH".....'None Type' object has no attribute '_sa_instance_state'
	# # .....sqlalchemy.orm.exc.UnmappedInstanceError: Class 'builtins.NoneType' is not mapped

# ...
if __name__ == "__main__":
	unittest.main()			#verbosity=2