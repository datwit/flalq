#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is customers test
"""

# import de module unittest2 that we need to create test
import json
import unittest2 as unittest
from api.utils.test_base import BaseTestCase
from api.utils.database import session
from api.models.offices import OfficeSchema
from api.models.employees import EmployeeSchema


office_schema = OfficeSchema()
employee_schema = EmployeeSchema()


def create_customer(self):
	""" This is 'create_customer' method to create customers using the SQLAlchemy model to facilitate testing. """

	office = {'officeCode': 'OF1', 'city': 'New York', 'phone': '111', 'addressLine1': 'Central Park', 'addressLine2': 'London', 'state': 'NY', 'country': 'usa', 'postalCode': '889000', 'territory': 'NA'}
	employee = {'employeeNumber': 1, 'lastName': 'Personal', 'firstName': 'Boss', 'extension': 'Administration', 'email': 'boss@yahoo.com', 'officeCode': 'OF1', 'jobTitle': 'Manager'}

	try:
		session.add(office_schema.load(office))
		session.add(employee_schema.load(employee))
	except Exception as e:
		session.rollback()
	finally:
		session.commit()


class TestCustomer(BaseTestCase):
	""" This is 'TestCustomer' class to hold all our tests. Import our base test class. """

	def setUp(self):
		""" This method set up the test client and call create_customer() method to create the customers. """
		super(TestCustomer, self).setUp()
		create_customer(self)

		self.customer1 = {'customerNumber': 2, 'customerName': 'Customer2', 'contactLastName': 'freedom', 'contactFirstName': 'two', 'phone': '222', 'addressLine1': 'Park', 'addressLine2': '41', 'city' : 'Miami', 'state' : 'FL', 'postalCode': '887833', 'country' : 'usa', 'salesRepEmployeeNumber' : 1, 'creditLimit': 70.5}

	def test_create_customer(self):
		""" Test to create a new customer with correct fields, using POST customer endpoint. """

		response = self.client.post('/customers/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.customer1))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(201, response.status_code)


	def test_create_customer_same_customerNumber(self):
		""" Test to try to create a new customer with an existing 'customerNumber'; which is key field, using POST customer endpoint. """

		response = self.client.post('/customers/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.customer1))
		customer = {'customerNumber': 2, 'customerName': 'Customer3', 'contactLastName': 'dom', 'contactFirstName': 'three', 'phone': '333', 'addressLine1': 'Ork', 'addressLine2': '16', 'city' : 'Miami', 'state' : 'FL', 'postalCode': '887833', 'country' : 'usa', 'salesRepEmployeeNumber' : 1, 'creditLimit': 85}
		response = self.client.post('/customers/', headers={'Content-Type': 'application/json'}, data=json.dumps(customer))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(422, response.status_code)


	def test_create_customer_with_empty_request(self):
		""" Test try to create a new customer without data; using POST customer endpoint. """

		customer = {}
		response = self.client.post('/customers/', headers={'Content-Type': 'application/json'}, data=json.dumps(customer))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(400, response.status_code)


	def test_create_customer_with_no_customerNumber(self):
		""" Test try to create a new customer without 'customerNumber'; which is key data, using POST customer endpoint. """

		customer = {'customerName': 'Customer5', 'contactLastName': 'dominic', 'contactFirstName': 'five', 'phone': '555', 'addressLine1': 'Ork', 'addressLine2': 'B', 'city' : 'Miami', 'state' : 'FL', 'postalCode': '887833', 'country' : 'usa', 'salesRepEmployeeNumber' : 1, 'creditLimit': 120}
		response = self.client.post('/customers/', headers={'Content-Type': 'application/json'}, data=json.dumps(customer))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(400, response.status_code)


	def test_delete_specific_customer(self):
		""" Test to get only one demanded customer, using GET customer by 'customerNumber' endpoint. """

		response = self.client.post('/customers/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.customer1))
		data = json.loads(response.data)
		print(data)
		response = self.client.delete('/customers/2', content_type='application/json')
		self.assertEqual(204, response.status_code)


	def test_get_customers(self):
		""" Test to get all customers, using GET all endpoint. """

		response = self.client.post('/customers/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.customer1))
		response = self.client.get('/customers/', content_type='application/json')
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


	def test_get_customer_details(self):
		""" Test to get only one demanded customer, using GET customer by 'customerNumber' endpoint. """

		response = self.client.post('/customers/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.customer1))
		response = self.client.get('/customers/2', content_type='application/json')
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


	def test_update_customer(self):
		""" Test to update some details in only one customer, using PUT customer by 'customerNumber' endpoint. """

		response = self.client.post('/customers/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.customer1))
		customer = {'customerNumber': 2, 'customerName': 'Customer6', 'contactLastName': 'john', 'contactFirstName': 'six', 'phone': '777', 'addressLine1': 'Ocean', 'addressLine2': 'A', 'city' : 'Miami', 'state' : 'FL', 'postalCode': '887833', 'country' : 'usa', 'salesRepEmployeeNumber' : 1, 'creditLimit': 235}
		response = self.client.put('/customers/2', headers={'Content-Type': 'application/json'}, data=json.dumps(customer))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)

	def test_update_customer_details(self):
		""" Test to update some details in only one customer, using PATCH customer by 'customerNumber' endpoint. """

		response = self.client.post('/customers/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.customer1))
		customer = {'customerNumber': 1, 'phone': '777', 'addressLine1': 'Ocean', 'addressLine2': 'A', 'postalCode': '887833'}
		response = self.client.patch('/customers/2', headers={'Content-Type': 'application/json'}, data=json.dumps(customer))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


# ...
if __name__ == "__main__":
	unittest.main()			#verbosity=2