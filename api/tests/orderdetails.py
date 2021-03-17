#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is orderdetails test
"""

# import de module unittest2 that we need to create test
import json
import unittest2 as unittest
from api.utils.test_base import BaseTestCase
from api.utils.database import session
from api.models.offices import OfficeSchema
from api.models.employees import EmployeeSchema
from api.models.customers import CustomerSchema
from api.models.orders import OrderSchema
from api.models.productlines import ProductlineSchema
from api.models.products import ProductSchema


office_schema = OfficeSchema()
employee_schema = EmployeeSchema()
customer_schema = CustomerSchema()
order_schema = OrderSchema()
productline_schema = ProductlineSchema()
product_schema = ProductSchema()


def create_orderdetail(self):
	""" This is 'create_orderdetail' method to create orderdetails using the SQLAlchemy model to facilitate testing. """

	office = {'officeCode': 'OF1', 'city': 'New York', 'phone': '111', 'addressLine1': 'Central Park', 'addressLine2': 'London', 'state': 'NY', 'country': 'usa', 'postalCode': '889000', 'territory': 'NA'}
	employee = {'employeeNumber': 1, 'lastName': 'Personal', 'firstName': 'Boss', 'extension': 'Administration', 'email': 'boss@yahoo.com', 'officeCode': 'OF1', 'jobTitle': 'Manager'}
	customer = {'customerNumber': 1, 'customerName': 'Customer1', 'contactLastName': 'Cuscus', 'contactFirstName': 'one', 'phone': '111', 'addressLine1': 'Park', 'addressLine2': '41', 'city' : 'Miami', 'state' : 'FL', 'postalCode': '887833', 'country' : 'usa', 'salesRepEmployeeNumber' : 1, 'creditLimit': 70.5}
	order = {'orderNumber': 1, 'orderDate': '2021-03-15 01:00:00', 'requiredDate': '2021-04-30', 'shippedDate': '2021-03-15', 'status': 'new', 'comments': 'null', 'customerNumber': 1}
	productline = {'productLine': 'Tools', 'textDescription': 'ome Tools', 'htmlDescription': 'html://shop.com/tools', 'image': ''}
	product = {'productCode': 'Drill', 'productName': 'drill master', 'productLine': 'Tools', 'productScale': '2', 'productVendor': 'DARK HORSE', 'productDescription': 'black metal', 'quantityInStock': 40, 'buyPrice': 80, 'MSRP': 100.0}

	try:
		session.add(office_schema.load(office))
		session.add(employee_schema.load(employee))
		session.add(customer_schema.load(customer))
		session.add(order_schema.load(order))
		session.add(productline_schema.load(productline))
		session.add(product_schema.load(product))
	except Exception as e:
		session.rollback()
	finally:
		session.commit()


class TestOrder(BaseTestCase):
	""" This is 'TestOrder' class to hold all our tests. Import our base test class. """

	def setUp(self):
		""" This method set up the test client and call create_orderdetail() method to create the orderdetails. """
		super(TestOrder, self).setUp()
		create_orderdetail(self)

		self.orderdetail1 = {'orderNumber': 1, 'productCode': 'Drill', 'quantityOrdered': 2, 'priceEach': 20, 'orderLineNumber': 1}

	def test_create_orderdetail(self):
		""" Test to create a new orderdetail with correct fields, using POST orderdetail endpoint. """

		response = self.client.post('/orderdetails/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.orderdetail1))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(201, response.status_code)


	def test_create_orderdetail_same_orderNumber_and_orderLineNumber(self):
		""" Test to create a new orderdetail with correct fields, using POST orderdetail endpoint. """

		response = self.client.post('/orderdetails/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.orderdetail1))
		orderdetail = {'orderNumber': 1, 'productCode': 'Drill', 'quantityOrdered': 3, 'priceEach': 20, 'orderLineNumber': 1}
		response = self.client.post('/orderdetails/', headers={'Content-Type': 'application/json'}, data=json.dumps(orderdetail))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(422, response.status_code)


	def test_create_orderdetail_with_no_orderNumber(self):
		""" Test try to create a new orderdetail without 'orderNumber'; which is key data, using POST orderdetail endpoint. """

		orderdetail = {'orderNumber': 1, 'productCode': 'Meter', 'quantityOrdered': 10, 'priceEach': 3, 'orderLineNumber': 1}
		response = self.client.post('/orderdetails/', headers={'Content-Type': 'application/json'}, data=json.dumps(orderdetail))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(400, response.status_code)


	def test_create_orderdetail_with_empty_request(self):
		""" Test try to create a new orderdetail without data; using POST orderdetail endpoint. """

		orderdetail = {}
		response = self.client.post('/orderdetails/', headers={'Content-Type': 'application/json'}, data=json.dumps(orderdetail))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(400, response.status_code)


	def test_get_orderdetails(self):
		""" Test to get all orderdetails, using GET all endpoint. """

		response = self.client.post('/orderdetails/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.orderdetail1))
		response = self.client.get('/orderdetails/', content_type='application/json')
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


	def test_get_orderdetail_details(self):
		""" Test to get only one demanded orderdetail, using GET orderdetail by 'orderNumber' endpoint. """

		response = self.client.post('/orderdetails/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.orderdetail1))
		response = self.client.get('/orderdetails/1/Drill', content_type='application/json')
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


	def test_delete_specific_orderdetail(self):
		""" Test to get only one demanded productline, using DELETE orderdetail by 'productLine' endpoint. """

		response = self.client.post('/orderdetails/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.orderdetail1))
		data = json.loads(response.data)
		print(data)
		response = self.client.delete('/orderdetails/1/Drill', content_type='application/json')
		self.assertEqual(204, response.status_code)


	def test_update_specific_orderdetail(self):
		""" Test to try to update quantityOrdered in one orderdetail, using PATCH productline by 'productLine' endpoint. """

		response = self.client.post('/orderdetails/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.orderdetail1))
		data = json.loads(response.data)
		print(data)
		orderdetail = {'orderNumber': 1, 'productCode': 'Meter', 'quantityOrdered': 10}
		response = self.client.patch('/orderdetails/1/Drill', headers={'Content-Type': 'application/json'}, data=json.dumps(orderdetail))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


	def test_update_specific_orderdetail_with_invalid_data(self):
		""" Test to try to update quantityOrdered in one orderdetail, using PATCH productline by 'productLine' endpoint, passing quantity superior than de stock. """

		response = self.client.post('/orderdetails/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.orderdetail1))
		data = json.loads(response.data)
		print(data)
		orderdetail = {'orderNumber': 1, 'productCode': 'Meter', 'quantityOrdered': 50}
		response = self.client.patch('/orderdetails/1/Drill', headers={'Content-Type': 'application/json'}, data=json.dumps(orderdetail))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(400, response.status_code)


# ...
if __name__ == "__main__":
	unittest.main()			#verbosity=2