#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is orders test
"""

# import de module unittest2 that we need to create test
import json
import unittest2 as unittest
from api.utils.test_base import BaseTestCase
from api.utils.database import session
from api.models.offices import OfficeSchema
from api.models.employees import EmployeeSchema
from api.models.customers import CustomerSchema


office_schema = OfficeSchema()
employee_schema = EmployeeSchema()
customer_schema = CustomerSchema()


def create_order(self):
	""" This is 'create_order' method to create orders using the SQLAlchemy model to facilitate testing. """

	office = {'officeCode': 'OF1', 'city': 'New York', 'phone': '111', 'addressLine1': 'Central Park', 'addressLine2': 'London', 'state': 'NY', 'country': 'usa', 'postalCode': '889000', 'territory': 'NA'}
	employee = {'employeeNumber': 1, 'lastName': 'Personal', 'firstName': 'Boss', 'extension': 'Administration', 'email': 'boss@yahoo.com', 'officeCode': 'OF1', 'jobTitle': 'Manager'}
	customer = {'customerNumber': 1, 'customerName': 'Customer2', 'contactLastName': 'freedom', 'contactFirstName': 'two', 'phone': '222', 'addressLine1': 'Park', 'addressLine2': '41', 'city' : 'Miami', 'state' : 'FL', 'postalCode': '887833', 'country' : 'usa', 'salesRepEmployeeNumber' : 1, 'creditLimit': 70.5}

	try:
		session.add(office_schema.load(office))
		session.add(employee_schema.load(employee))
		session.add(customer_schema.load(customer))
	except Exception as e:
		session.rollback()
	finally:
		session.commit()


class TestOrder(BaseTestCase):
	""" This is 'TestOrder' class to hold all our tests. Import our base test class. """

	def setUp(self):
		""" This method set up the test client and call create_order() method to create the orders. """
		super(TestOrder, self).setUp()
		create_order(self)

		self.order1 = {'orderNumber': 1, 'orderDate': '2021-03-15 01:00:00', 'requiredDate': '2021-04-30', 'shippedDate': '2021-03-15', 'status': 'new', 'comments': 'null', 'customerNumber': 1}


	def test_create_order(self):
		""" Test to create a new order with correct fields, using POST order endpoint. """

		response = self.client.post('/orders/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.order1))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(201, response.status_code)


	def test_create_order_same_orderNumber(self):
		""" Test to try to create a new order with an existing 'orderNumber'; which is key field, using POST order endpoint. """

		response = self.client.post('/orders/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.order1))
		order = {'orderNumber': 1, 'orderDate': '2021-03-15 02:00:00', 'requiredDate': '2021-04-30', 'shippedDate': '2021-03-15', 'status': 'new', 'comments': 'existing', 'customerNumber': 1}
		response = self.client.post('/orders/', headers={'Content-Type': 'application/json'}, data=json.dumps(order))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(422, response.status_code)


	def test_create_order_with_no_orderNumber(self):
		""" Test try to create a new order without 'orderNumber'; which is key data, using POST order endpoint. """

		order = {'orderDate': '2021-03-15 03:00:00', 'requiredDate': '2021-04-30', 'shippedDate': '2021-03-15', 'status': 'new', 'comments': 'incorrect data', 'customerNumber': 1}
		response = self.client.post('/orders/', headers={'Content-Type': 'application/json'}, data=json.dumps(order))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(400, response.status_code)


	def test_create_order_with_empty_request(self):
		""" Test try to create a new order without data; using POST order endpoint. """

		order = {}
		response = self.client.post('/orders/', headers={'Content-Type': 'application/json'}, data=json.dumps(order))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(400, response.status_code)


	def test_delete_specific_order(self):
		""" Test to get only one demanded order, using GET order by 'orderNumber' endpoint. """

		response = self.client.post('/orders/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.order1))
		data = json.loads(response.data)
		print(data)
		response = self.client.delete('/orders/1', content_type='application/json')
		self.assertEqual(204, response.status_code)


	def test_get_orders(self):
		""" Test to get all orders, using GET all endpoint. """

		response = self.client.post('/orders/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.order1))
		response = self.client.get('/orders/', content_type='application/json')
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


	def test_get_order_details(self):
		""" Test to get only one demanded order, using GET order by 'orderNumber' endpoint. """

		response = self.client.post('/orders/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.order1))
		response = self.client.get('/orders/1', content_type='application/json')
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


	def test_update_order(self):
		""" Test to update some details in only one order, using PUT order by 'orderNumber' endpoint. """

		response = self.client.post('/orders/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.order1))
		order = {'orderNumber': 1, 'orderDate': '2021-03-15 04:00:00', 'requiredDate': '2021-03-31', 'shippedDate': '2021-03-15', 'status': 'transporting', 'comments': 'to client', 'customerNumber': 1}
		response = self.client.put('/orders/1', headers={'Content-Type': 'application/json'}, data=json.dumps(order))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


	def test_update_order_details(self):
		""" Test to update some details in only one order, using PATCH order by 'orderNumber' endpoint. """

		response = self.client.post('/orders/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.order1))
		order = {'orderNumber': 1, 'requiredDate': '2021-03-31', 'shippedDate': '2021-03-15', 'status': 'transporting', 'comments': 'to client'}
		response = self.client.patch('/orders/1', headers={'Content-Type': 'application/json'}, data=json.dumps(order))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


	# # "PATCH".....'None Type' object has no attribute '_sa_instance_state'
	# # .....sqlalchemy.orm.exc.UnmappedInstanceError: Class 'builtins.NoneType' is not mapped

# ...
if __name__ == "__main__":
	unittest.main()			#verbosity=2