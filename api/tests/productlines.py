#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is productlines test
"""

# import de module unittest2 that we need to create test
import json
import unittest2 as unittest
from api.utils.test_base import BaseTestCase
from os import open
import io
import os
from pathlib import Path


class TestProductline(BaseTestCase):
	""" This is 'TestProductLine' class to hold all our tests. Import our base test class. """

	def setUp(self):
		""" This method set up the test client and call create_productline() method to create the productlines. """
		super(TestProductline, self).setUp()

		self.productline1 = {'productLine': 'DFood', 'textDescription': 'Dog Food', 'htmlDescription': 'html://shop.com/dogfood', 'image': ''}

	def test_create_productline(self):
		""" Test to create a new productline with correct fields, using POST productline endpoint. """

		response = self.client.post('/productlines/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.productline1))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(201, response.status_code)


	# def test_create_image_productline(self):
	# 	""" Test to create a productline image, using POST productline image endpoint. """

	# 	folder = Path(r"C:\Users\Danay\Pictures\tests_api")
	# 	destiny = Path(r"C:\Users\Danay\Desktop\danay_python\snippets\api_classic\api\images\")
	# 	response = self.client.post('/productlines/', content_type='application/json', data=json.dumps(self.productline1))
	# 	data = json.loads(response.data)
	# 	print(data)
	# 	# response = self.client.post('/productlines/image/DFood', data=dict(file=(io.BytesIO(b"this is a test"), 'api_test_file.jpg')),  content_type='multipart/form-data')

	# 	# response = self.client.post('/productlines/image/DFood', data={'image': 'C:/Users/Danay/Pictures/test_api/api_test_file.jpg'}, content_type='multipart/form-data')

	# 	response = self.client.post('/productlines/image/DFood', data={'image': [open(folder, 'rb')], 'destiny': destiny})
	# 	# response = self.client.post('/productlines/image/DFood', data={'image': (io.BytesIO(b"this is a test"), 'api_test_file.jpg')},  content_type='multipart/form-data')
	# 	print(response.data)
	# 	self.assertEqual(201, response.status_code)


	def test_create_productline_same_productLine(self):
		""" Test to try to create a new productline with an existing 'productLine'; which is key field, using POST productline endpoint. """

		response = self.client.post('/productlines/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.productline1))
		productline = {'productLine': 'DFood', 'textDescription': 'dog food', 'htmlDescription': 'html://shop..dog.com', 'image': ''}
		response = self.client.post('/productlines/', headers={'Content-Type': 'application/json'}, data=json.dumps(productline))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(422, response.status_code)


	def test_create_productline_with_no_productLine(self):
		""" Test try to create a new productline without 'productLine'; which is key data, using POST productline endpoint. """

		productline = {'textDescription': 'cat food', 'htmlDescription': 'html://shop.cat.com', 'image': ''}
		response = self.client.post('/productlines/', headers={'Content-Type': 'application/json'}, data=json.dumps(productline))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(400, response.status_code)

	def test_create_productline_with_empty_request(self):
		""" Test try to create a new productline without data; using POST productline endpoint. """

		productline = {}
		response = self.client.post('/productlines/', headers={'Content-Type': 'application/json'}, data=json.dumps(productline))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(400, response.status_code)


	def test_delete_specific_productline(self):
		""" Test to get only one demanded productline, using DELETE productline by 'productLine' endpoint. """

		response = self.client.post('/productlines/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.productline1))
		data = json.loads(response.data)
		print(data)
		response = self.client.delete('/productlines/DFood', content_type='application/json')
		self.assertEqual(204, response.status_code)


	def test_get_productlines(self):
		""" Test to get all productlines, using GET all endpoint. """

		response = self.client.post('/productlines/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.productline1))
		response = self.client.get('/productlines/', content_type='application/json')
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


	def test_get_productline_details(self):
		""" Test to get only one demanded productline, using GET productline by 'productLine' endpoint. """

		response = self.client.post('/productlines/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.productline1))
		response = self.client.get('/productlines/DFood', content_type='application/json')
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


	def test_update_productline(self):
		""" Test to update some details in only one productline, using PUT productline by 'productLine' endpoint. """

		response = self.client.post('/productlines/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.productline1))
		productline = {'productLine': 'DFood', 'textDescription': 'Dog vegetal food', 'htmlDescription': 'html://shop.food.com/vegetal', 'image': ''}
		response = self.client.put('/productlines/DFood', headers={'Content-Type': 'application/json'}, data=json.dumps(productline))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


	def test_update_productline_details(self):
		""" Test to update some details in only one productline, using PATCH productline by 'productLine' endpoint. """

		response = self.client.post('/productlines/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.productline1))
		productline = {'productLine': 'DFood', 'textDescription': 'Dog vegetal food', 'htmlDescription': 'html://shop.food.com/vegetal'}
		response = self.client.patch('/productlines/DFood', headers={'Content-Type': 'application/json'}, data=json.dumps(productline))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


# ...
if __name__ == "__main__":
	unittest.main()			#verbosity=2