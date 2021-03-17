#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is products test
"""

# import de module unittest2 that we need to create test
import json
import unittest2 as unittest
from api.utils.test_base import BaseTestCase
from api.utils.database import session
from api.models.productlines import ProductlineSchema
from api.models.products import ProductSchema


productline_schema = ProductlineSchema()
product_schema = ProductSchema()


def create_product(self):
	""" This is 'create_product' method to create products using the SQLAlchemy model to facilitate testing. """

	productline = {'productLine': 'Tools', 'textDescription': 'Home Mechanic Tools', 'htmlDescription': 'html://shop.home.com/Tools', 'image': ''}

	try:
		session.add(productline_schema.load(productline))
	except Exception as e:
		session.rollback()
	finally:
		session.commit()


class TestProduct(BaseTestCase):
	""" This is 'TestProduct' class to hold all our tests. Import our base test class. """

	def setUp(self):
		""" This method set up the test client and call create_product() method to create the products. """
		super(TestProduct, self).setUp()
		create_product(self)

		self.product1 = {'productCode': 'drill', 'productName': 'drill master', 'productLine': 'Tools', 'productScale': '2', 'productVendor': 'DARK HORSE', 'productDescription': 'black metal', 'quantityInStock': 40, 'buyPrice': 80, 'MSRP': 100.0}


	def test_create_product(self):
		""" Test to create a new product with correct fields, using POST product endpoint. """

		response = self.client.post('/products/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.product1))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(201, response.status_code)

	def test_create_product_same_productCode(self):
		""" Test to try to create a new product with an existing 'productCode'; which is key field, using POST product endpoint. """

		response = self.client.post('/products/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.product1))
		product = {'productCode': 'drill', 'productName': 'drill blue', 'productLine': 'Tools', 'productScale': '3', 'productVendor': 'LIGHT HORSE', 'productDescription': 'pink metal', 'quantityInStock': 30, 'buyPrice': 60, 'MSRP': 100}
		response = self.client.post('/products/', headers={'Content-Type': 'application/json'}, data=json.dumps(product))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(422, response.status_code)


	def test_create_product_with_no_productCode(self):
		""" Test try to create a new product without 'productCode'; which is key data, using POST product endpoint. """

		product = {'productName': 'drill green', 'productLine': 'Tools', 'productScale': '4', 'productVendor': 'LIGHT', 'productDescription': 'red', 'quantityInStock': 50, 'buyPrice': 100, 'MSRP': 100}
		response = self.client.post('/products/', headers={'Content-Type': 'application/json'}, data=json.dumps(product))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(400, response.status_code)


	def test_create_product_with_empty_request(self):
		""" Test try to create a new product without data; using POST product endpoint. """

		product = {}
		response = self.client.post('/products/', headers={'Content-Type': 'application/json'}, data=json.dumps(product))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(400, response.status_code)


	def test_delete_specific_productline(self):
		""" Test to get only one demanded product, using GET product by 'productCode' endpoint. """

		response = self.client.post('/products/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.product1))
		data = json.loads(response.data)
		print(data)
		response = self.client.delete('/products/drill', content_type='application/json')
		self.assertEqual(204, response.status_code)


	def test_get_products(self):
		""" Test to get all products, using GET all endpoint. """

		response = self.client.post('/products/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.product1))
		response = self.client.get('/products/', content_type='application/json')
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


	def test_get_product_details(self):
		""" Test to get only one demanded product, using GET product by 'productCode' endpoint. """

		response = self.client.post('/products/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.product1))
		response = self.client.get('/products/drill', content_type='application/json')
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


	def test_update_productline(self):
		""" Test to update some details in only one product, using PUT product by 'productCode' endpoint. """

		response = self.client.post('/products/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.product1))
		product = {'productCode': 'drill', 'productName': 'circular drill', 'productLine': 'Tools', 'productScale': '5', 'productVendor': 'BOSH', 'productDescription': 'black and blue colors', 'quantityInStock': 60, 'buyPrice': 120, 'MSRP': 100}
		response = self.client.put('/products/drill', headers={'Content-Type': 'application/json'}, data=json.dumps(product))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


	def test_update_productline_details(self):
		""" Test to update some details in only one product, using PATCH product by 'productCode' endpoint. """

		response = self.client.post('/products/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.product1))
		product = {'productCode': 'drill', 'productVendor': 'BOSH', 'productDescription': 'black and blue colors', 'buyPrice': 120,}
		response = self.client.patch('/products/drill', headers={'Content-Type': 'application/json'}, data=json.dumps(product))
		data = json.loads(response.data)
		print(data)
		self.assertEqual(200, response.status_code)


# ...
if __name__ == "__main__":
	unittest.main()			#verbosity=2