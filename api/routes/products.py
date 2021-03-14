#!/usr/bin/python
# -*- coding: utf-8 -*-
""""

"""

from flask import Blueprint, request
from api.models.products import Product, ProductSchema
from api.utils.database import session, engine
from api.utils import responses as resp
from sqlalchemy import text


product_routes = Blueprint("product_routes", __name__)
object_schema = ProductSchema()

# Create a URL route in our application for "/products/" to read a collection
@product_routes.route('/products/', methods=['GET'])
def allproducts():
    rows = session.query(Product).all()
    result = object_schema.dump(rows, many=True)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


# Create a URL route in our application for "/products/" to create a new row
@product_routes.route('/products/', methods=['POST'])
def postproduct():
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "No input data provided"}), resp.BAD_REQUEST_400
    elif data.get('productCode'):
        found = session.query(Product).get(data["productCode"])
        if not found:
            try:
                row = object_schema.load(data)
                session.add(row)
                session.commit()
                result = object_schema.dump(session.query(Product).get(data["productCode"]))
                return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
            except Exception as e:
                session.rollback()
                return resp.response_with(resp.BAD_REQUEST_400, value={"error": str(e)}), resp.BAD_REQUEST_400
        else:
            return resp.response_with(resp.INVALID_FIELD_NAME_SENT_422, value={"error": "Key data already exists"}), resp.INVALID_FIELD_NAME_SENT_422
    else:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "Data no has key field"}), resp.BAD_REQUEST_400


# Create a URL route in our application for "/products/" to read a particular row in the collection
@product_routes.route('/products/<string:productCode>', methods=['GET'])
def getproducts(productCode):
    productCode_found = productCode
    found = session.query(Product).get(productCode_found)
    if not found:
        return resp.response_with(resp.SERVER_ERROR_404, value={"error": "The request data no exists"}), resp.SERVER_ERROR_404
    else:
        result = object_schema.dump(found)
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200


# Create a URL route in our application for "/products/" to update all details of an existing row
@product_routes.route('/products/<string:productCode>', methods=['PUT'])
def putproducts(productCode):
    productCode_found = productCode
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "No input data provided"}), resp.BAD_REQUEST_400
    elif data.get('productCode'):
        found = session.query(Product).get(productCode_found)
        if found:
            try:
                row = object_schema.dump(data)
                session.query(Product).filter(Product.productCode==productCode_found).update(row)
                session.commit()
                result = object_schema.dump(found)
                return resp.response_with(resp.SUCCESS_200, value={"Updated Row": result}), resp.SUCCESS_200
            except Exception as e:
                session.rollback()
                return resp.response_with(resp.BAD_REQUEST_400, value={"error": str(e)}), resp.BAD_REQUEST_400
        else:
            return resp.response_with(resp.INVALID_FIELD_NAME_SENT_422, value={"error": "The request data no exists"}), resp.INVALID_FIELD_NAME_SENT_422
    else:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "Data no has key field"}), resp.BAD_REQUEST_400


# Create a URL route in our application for "/products/" to update some details of an existing row
@product_routes.route('/products/<string:productCode>', methods=['PATCH'])
def patchoffice(productCode):
    productCode_found = productCode
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "No input data provided"}), resp.BAD_REQUEST_400
    elif data.get('productCode'):
        found = session.query(Product).get(productCode_found)
        if found:
            try:
                if data.get('productVendor'):
                    found.productVendor = data['productVendor']
                if data.get('productDescription'):
                    found.productDescription = data['productDescription']
                if data.get('buyPrice'):
                    found.buyPrice = data['buyPrice']
                session.add(row)
                session.commit()
                result = object_schema.dump(found)
                return resp.response_with(resp.SUCCESS_200, value={"Updated Row Fields": result}), resp.SUCCESS_200
            except Exception as e:
                session.rollback()
                return resp.response_with(resp.BAD_REQUEST_400, value={"error": str(e)}), resp.BAD_REQUEST_400
        else:
            return resp.response_with(resp.INVALID_FIELD_NAME_SENT_422, value={"error": "The request data no exists"}), resp.INVALID_FIELD_NAME_SENT_422
    else:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "Data no has key field"}), resp.BAD_REQUEST_400


# Create a URL route in our application for "/products/" to delete an existing row
@product_routes.route('/products/<string:productCode>', methods=['DELETE'])
def delproducts(productCode):
    productCode_found = productCode
    found = session.query(Product).get(productCode_found)
    if found:
        try:
            session.delete(found)
            session.commit()
            return resp.response_with(resp.SUCCESS_204, value={'message': 'Deleted Row'}), resp.SUCCESS_204
        except Exception as e:
            session.rollback()
            return resp.response_with(resp.BAD_REQUEST_400, value={"error": str(e)}), resp.BAD_REQUEST_400
    else:
        return resp.response_with(resp.SERVER_ERROR_404, value={"error": "The request data no exists"}), resp.SERVER_ERROR_404