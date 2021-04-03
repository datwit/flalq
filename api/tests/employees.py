#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is employees test
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


def create_employee(self):
	""" This is 'create_employee' method to create employees using the SQLAlchemy model to facilitate testing. """

	office = {'officeCode': 'OF1', 'city': 'New York', 'phone': '111', 'addressLine1': 'Central Park', 'addressLine2': 'London', 'state': 'NY', 'country': 'usa', 'postalCode': '889000', 'territory': 'NA'}
	employee = {'employeeNumber': 1, 'lastName': 'Personal', 'firstName': 'Boss', 'extension': 'Administration', 'email': 'boss@yahoo.com', 'officeCode': 'OF1', 'jobTitle': 'Manager'}
	try:
		session.add(office_schema.load(office))
		session.add(employee_schema.load(employee))
	except Exception as e:
		session.rollback()
	finally:
		session.commit()


class TestEmployee(BaseTestCase):
	""" This is 'TestEmployee' class to hold all our tests. Import our base test class. """

	def setUp(self):
		""" This method set up the test client and call create_employees() method to create the employees. """
		super(TestEmployee, self).setUp()
		create_employee(self)

		self.employee1 = {'employeeNumber': 2, 'lastName': 'Employee', 'firstName': 'First', 'extension': 'Food', 'email': 'fierst@yahoo.com', 'officeCode': 'OF1', 'reportsTo': 1, 'jobTitle': 'shopman'}


	def test_create_employee(self):
		""" Test to create a new employee with correct fields, using POST employee endpoint. """

		response = self.client.post('/employees/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.employee1))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(201, response.status_code)


	def test_create_employee_same_employeeNumber(self):
		""" Test to try to create a new employee with an existing 'employeeNumber'; which is key field, using POST employee endpoint. """

		response = self.client.post('/employees/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.employee1))
		employee2 = {'employeeNumber': 2, 'lastName': 'Employee', 'firstName': 'Second', 'extension': 'Food', 'email': 'second@yahoo.com', 'officeCode': 'OF1', 'reportsTo': 1, 'jobTitle': 'shopman'}
		response = self.client.post('/employees/', headers={'Content-Type': 'application/json'}, data=json.dumps(employee2))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(422, response.status_code)


	def test_create_employee_with_empty_request(self):
		""" Test try to create a new employee without data; using POST employee endpoint. """

		employee = {}
		response = self.client.post('/employees/', headers={'Content-Type': 'application/json'}, data=json.dumps(employee))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(400, response.status_code)


	def test_create_employee_with_no_employeeNumber(self):
		""" Test try to create a new employee without 'employeeNumber'; which is key data, using POST employee endpoint. """

		employee = {'lastName': "Employee", 'firstName': "Five", 'extension': "Tools", 'email': "five@yahoo.com", 'officeCode': 'OF1', 'reportsTo': 1, 'jobTitle': "shopman"}
		response = self.client.post('/employees/', headers={'Content-Type': 'application/json'}, data=json.dumps(employee))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(400, response.status_code)


	def test_delete_specific_employee(self):
		""" Test to get only one demanded employee, using GET employee by 'employeeNumber' endpoint. """

		response = self.client.post('/employees/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.employee1))
		data = json.loads(response.data)
		print(data)
		response = self.client.delete('/employees/2', content_type='application/json')
		self.assertEqual(204, response.status_code)


	def test_get_employees(self):
		""" Test to get all employees, using GET all endpoint. """

		response = self.client.get('/employees/', content_type='application/json')
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


	def test_get_employee_details(self):
		""" Test to get only one demanded employee, using GET employee by 'employeeNumber' endpoint. """

		response = self.client.post('/employees/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.employee1))
		response = self.client.get('/employees/2', content_type='application/json')
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


	def test_update_employee(self):
		""" Test to update some details in only one employee, using PUT employee by 'employeeNumber' endpoint. """

		response = self.client.post('/employees/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.employee1))
		employee = {'employeeNumber': 2, 'lastName': "Manager", 'firstName': "Second", 'extension': "Administration", 'email': "second@yahoo.com", 'officeCode': "OF1", 'reportsTo': 1, 'jobTitle': "web_master"}
		response = self.client.put('/employees/2', headers={'Content-Type': 'application/json'}, data=json.dumps(employee))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


	def test_update_employee_details(self):
		""" Test to update some details in only one employee, using PATCH employee by 'employeeNumber' endpoint. """

		response = self.client.post('/employees/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.employee1))
		employee = {'employeeNumber': 2, 'extension': "Administration", 'officeCode': "OF1", 'reportsTo': 1, 'jobTitle': "web_master"}
		response = self.client.patch('/employees/2', headers={'Content-Type': 'application/json'}, data=json.dumps(employee))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


# ...
if __name__ == "__main__":
	unittest.main(verbosity=2)			#verbosity=2