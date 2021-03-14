#!/usr/bin/python
# -*- coding: utf-8 -*-
""""

"""

from flask import Blueprint, request
from api.models.orderdetails import Orderdetail, OrderdetailSchema
from api.models.products import Product
from api.utils.database import session, engine
from api.utils import responses as resp
from sqlalchemy import text


orderdetail_routes = Blueprint("orderdetail_routes", __name__)
object_schema = OrderdetailSchema()

# Create a URL route in our application for "/orderdetails/" to read a collection
@orderdetail_routes.route('/orderdetails/', methods=['GET'])
def allorderdetails():
    rows = session.query(Orderdetail).all()
    result = object_schema.dump(rows, many=True)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


# Create a URL route in our application for "/orderdetails/" to create a new row
@orderdetail_routes.route('/orderdetails/', methods=['POST'])
def postorderdetail():
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "No input data provided"}), resp.BAD_REQUEST_400
    elif data.get('orderNumber') and data.get('productCode'):
        found = session.query(Orderdetail).get({"orderNumber": data["orderNumber"], "productCode": data["productCode"]})
        if not found:
            try:
                row = object_schema.load(data)
                product_data = data['productCode']
                quantity_data = data['quantityOrdered']
                product_ordered = session.query(Product).get(product_data)
                quantity_stock = product_ordered.quantityInStock
                if quantity_data <= quantity_stock:
                    session.add(row)
                    quantity_stock = quantity_stock - quantity_data
                    product_ordered.quantityInStock = quantity_stock
                    session.commit()
                    result = object_schema.dump(session.query(Orderdetail).get({"orderNumber": data["orderNumber"], "productCode": data["productCode"]}))
                    return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
                else:
                    return resp.response_with(resp.BAD_REQUEST_400, value={"Message": "Not have enough In Stock"}), resp.BAD_REQUEST_400
            except Exception as e:
                session.rollback()
                return resp.response_with(resp.BAD_REQUEST_400, value={"error": str(e)}), resp.BAD_REQUEST_400
        else:
            return resp.response_with(resp.INVALID_FIELD_NAME_SENT_422, value={"error": "Key data already exists"}), resp.INVALID_FIELD_NAME_SENT_422
    else:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "Data no has key field"}), resp.BAD_REQUEST_400


# Create a URL route in our application for "/orderdetails/" to read a particular row in the collection
@orderdetail_routes.route('/orderdetails/<int:orderNumber>/<string:productCode>', methods=['GET'])
def getorderdetails(orderNumber, productCode):
    order_found = orderNumber
    productCode_found = productCode
    found = session.query(Orderdetail).get({"orderNumber": order_found, "productCode": productCode_found})
    if not found:
        return resp.response_with(resp.SERVER_ERROR_404, value={"error": "The request data no exists"}), resp.SERVER_ERROR_404
    else:
        result = object_schema.dump(found)
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200


# Create a URL route in our application for "/orderdetails/" to update few details of an existing row
@orderdetail_routes.route('/orderdetails/<int:orderNumber>/<string:productCode>', methods=['PATCH'])
def putorderdetails(orderNumber, productCode):
    orderNumber_found = orderNumber
    productCode_found = productCode
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "No input data provided"}), resp.BAD_REQUEST_400
    elif data.get('orderNumber') and data.get('productCode'):
        found = session.query(Orderdetail).get({"orderNumber": orderNumber_found, "productCode": productCode_found})
        if found:
            try:
                quantity_data = data['quantityOrdered']
                # ordered_details = session.query(Orderdetail).get({"orderNumber": orderNumber_found, "productCode": productCode_found})
                quantity_before = found.quantityOrdered             #
                product_ordered = session.query(Product).get(found.productCode)           #
                quantity_stock = product_ordered.quantityInStock
                if quantity_data <= (quantity_stock + quantity_before):
                    found.quantityOrdered = quantity_data             #
                    session.commit()
                    quantity_stock = (quantity_stock + quantity_before) - quantity_data
                    product_ordered.quantityInStock = quantity_stock
                    session.commit()
                    result = object_schema.dump(found)
                    return resp.response_with(resp.SUCCESS_200, value={"Updated Row": result}), resp.SUCCESS_200
                else:
                    return resp.response_with(resp.BAD_REQUEST_400, value={"Message": "Not have enough In Stock"}), resp.BAD_REQUEST_400
            except Exception as e:
                session.rollback()
                return resp.response_with(resp.BAD_REQUEST_400, value={"error": str(e)}), resp.BAD_REQUEST_400
        else:
            return resp.response_with(resp.INVALID_FIELD_NAME_SENT_422, value={"error": "The request data no exists"}), resp.INVALID_FIELD_NAME_SENT_422
    else:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "Data no has key field"}), resp.BAD_REQUEST_400


# Create a URL route in our application for "/orderdetails/" to delete an existing row
@orderdetail_routes.route('/orderdetails/<int:orderNumber>/<string:productCode>', methods=['DELETE'])
def delorderdetails(orderNumber, productCode):
    orderNumber_found = orderNumber
    productCode_found = productCode
    found = session.query(Orderdetail).get({"orderNumber": orderNumber_found, "productCode": productCode_found})
    if found:
        try:
            quantity_product = found.quantityOrdered
            product_found = found.productCode
            session.delete(found)
            session.commit()
            product_ordered = session.query(Product).get(product_found)
            quantity_stock = product_ordered.quantityInStock
            product_ordered.quantityInStock = quantity_stock + quantity_product
            session.commit()
            return resp.response_with(resp.SUCCESS_204, value={'message': 'Deleted Row'}), resp.SUCCESS_204
        except Exception as e:
            session.rollback()
            return resp.response_with(resp.BAD_REQUEST_400, value={"error": str(e)}), resp.BAD_REQUEST_400
    else:
        return resp.response_with(resp.SERVER_ERROR_404, value={"error": "The request data no exists"}), resp.SERVER_ERROR_404