#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is payments test
"""

# import de module unittest2 that we need to create test
import json
import unittest2 as unittest
from api.utils.test_base import BaseTestCase
from api.utils.database import session
from api.models.offices import OfficeSchema
from api.models.employees import EmployeeSchema
from api.models.customers import CustomerSchema
import datetime as dt


office_schema = OfficeSchema()
employee_schema = EmployeeSchema()
customer_schema = CustomerSchema()


def create_payment(self):
	""" This is 'create_payment' method to create payments using the SQLAlchemy model to facilitate testing. """

	office = {'officeCode': 'OF1', 'city': 'New York', 'phone': '111', 'addressLine1': 'Central Park', 'addressLine2': 'London', 'state': 'NY', 'country': 'usa', 'postalCode': '889000', 'territory': 'NA'}
	employee = {'employeeNumber': 1, 'lastName': 'Personal', 'firstName': 'Boss', 'extension': 'Administration', 'email': 'boss@yahoo.com', 'officeCode': 'OF1', 'jobTitle': 'Manager'}
	customer = {'customerNumber': 1, 'customerName': 'Customer1', 'contactLastName': 'Cuscus', 'contactFirstName': 'one', 'phone': '111', 'addressLine1': 'Park', 'addressLine2': '41', 'city' : 'Miami', 'state' : 'FL', 'postalCode': '887833', 'country' : 'usa', 'salesRepEmployeeNumber' : 1, 'creditLimit': 70.5}

	try:
		session.add(office_schema.load(office))
		session.add(employee_schema.load(employee))
		session.add(customer_schema.load(customer))
	except Exception as e:
		session.rollback()
	finally:
		session.commit()


class TestPayment(BaseTestCase):
	""" This is 'TestCustomer' class to hold all our tests. Import our base test class. """

	def setUp(self):
		""" This method set up the test client and call create_payment() method to create the payments. """
		super(TestPayment, self).setUp()
		create_payment(self)

		self.payment1 = {'customerNumber': 1, 'checkNumber': 'HPP1001', 'paymentDate': '2020-03-01', 'amount': 120.0}


	def test_create_payment(self):
		""" Test to create a new payment with correct fields, using POST payment endpoint. """

		response = self.client.post('/payments/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.payment1))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(201, response.status_code)


	def test_create_payment_same_checkNumber(self):
		""" Test to try to create a new payment with an existing 'checkNumber'; which is key field, using POST payment endpoint. """

		response = self.client.post('/payments/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.payment1))
		payment = {'customerNumber': 1, 'checkNumber': 'HPP1001', 'paymentDate': '2020-05-10', 'amount': 700}
		response = self.client.post('/payments/', headers={'Content-Type': 'application/json'}, data=json.dumps(payment))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(422, response.status_code)


	def test_create_payment_with_no_customerNumber(self):
		""" Test try to create a new payment without 'customerNumber'; which is key data, using POST payment endpoint. """

		payment = {'checkNumber': 'HPP1003', 'paymentDate': '2020-07-13', 'amount': 660}
		response = self.client.post('/payments/', headers={'Content-Type': 'application/json'}, data=json.dumps(payment))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(400, response.status_code)


	def test_create_payment_with_no_checkNumber(self):
		""" Test try to create a new payment without 'checkNumber'; which is key data, using POST payment endpoint. """

		payment = {'customerNumber': 1, 'paymentDate': '2020-09-17', 'amount': 810.0}
		response = self.client.post('/payments/', headers={'Content-Type': 'application/json'}, data=json.dumps(payment))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(400, response.status_code)


	def test_create_payment_with_empty_request(self):
		""" Test try to create a new payment without data; using POST payment endpoint. """

		payment = {}
		response = self.client.post('/payments/', headers={'Content-Type': 'application/json'}, data=json.dumps(payment))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(400, response.status_code)


	def test_delete_specific_checkNumber(self):
		""" Test to get only one demanded payment, using GET payment by 'checkNumber' endpoint. """

		response = self.client.post('/payments/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.payment1))
		data = json.loads(response.data)
		print(data)
		response = self.client.delete('/payments/1/HPP1001', content_type='application/json')
		self.assertEqual(204, response.status_code)


	def test_get_payments(self):
		""" Test to get all payments, using GET all endpoint. """

		response = self.client.post('/payments/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.payment1))
		response = self.client.get('/payments/', content_type='application/json')
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)

	def test_get_payment_details(self):
		""" Test to get only one demanded payment, using GET payment by 'checkNumber' endpoint. """

		response = self.client.post('/payments/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.payment1))
		response = self.client.get('/payments/1/HPP1001', content_type='application/json')
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


	def test_update_payment(self):
		""" Test to update some details in only one payment, using PUT payment by 'checkNumber' endpoint. """

		response = self.client.post('/payments/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.payment1))
		data = json.loads(response.data)
		print(data)
		payment = {'customerNumber': 1, 'checkNumber': 'HPP1001', 'paymentDate': '2020-03-01', 'amount': 2220}
		response = self.client.put('/payments/1/HPP1001', headers={'Content-Type': 'application/json'}, data=json.dumps(payment))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


# ...
if __name__ == "__main__":
	unittest.main()			#verbosity=2