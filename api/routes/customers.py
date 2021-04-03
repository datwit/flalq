#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""

from flask import Blueprint, request
from api.models.customers import Customer, CustomerSchema
from api.utils.database import session, engine
from api.utils import responses as resp
from sqlalchemy import text


customer_routes = Blueprint("customer_routes", __name__)
object_schema = CustomerSchema()

# Create a URL route in our application for "/customers/" to read a collection
@customer_routes.route('/customers/', methods=['GET'])
def allcustomers():
    rows = session.query(Customer).all()
    result = object_schema.dump(rows, many=True)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


# Create a URL route in our application for "/customers/" to create a new row
@customer_routes.route('/customers/', methods=['POST'])
def postcustomer():
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "No input data provided"}), resp.BAD_REQUEST_400
    elif data.get('customerNumber'):
        found = session.query(Customer).get(data["customerNumber"])
        if not found:
            try:
                row = object_schema.load(data)
                session.add(row)
                session.commit()
                result = object_schema.dump(session.query(Customer).get(data["customerNumber"]))
                return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
            except Exception as e:
                session.rollback()
                return resp.response_with(resp.BAD_REQUEST_400, value={"error": str(e)}), resp.BAD_REQUEST_400
        else:
            return resp.response_with(resp.INVALID_FIELD_NAME_SENT_422, value={"error": "Key data already exists"}), resp.INVALID_FIELD_NAME_SENT_422
    else:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "Data no has key field"}), resp.BAD_REQUEST_400


# Create a URL route in our application for "/customers/" to read a particular row in the collection
@customer_routes.route('/customers/<int:customerNumber>', methods=['GET'])
def getcustomer(customerNumber):
    customerNumber_found = customerNumber
    found = session.query(Customer).get(customerNumber_found)
    if not found:
        return resp.response_with(resp.SERVER_ERROR_404, value={"error": "The request data no exists"}), resp.SERVER_ERROR_404
    else:
        result = object_schema.dump(found)
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200


# Create a URL route in our application for "/customers/" to update all details of an existing row
@customer_routes.route('/customers/<int:customerNumber>', methods=['PUT'])
def putcustomer(customerNumber):
    customerNumber_found = customerNumber
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "No input data provided"}), resp.BAD_REQUEST_400
    elif data.get('customerNumber'):
        found = session.query(Customer).get(customerNumber_found)
        if found:
            try:
                row = object_schema.dump(data)
                session.query(Customer).filter(Customer.customerNumber==customerNumber_found).update(row)
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


# Create a URL route in our application for "/customers/" to update some details of an existing row
@customer_routes.route('/customers/<int:customerNumber>', methods=['PATCH'])
def patchoffice(customerNumber):
    customerNumber_found = customerNumber
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "No input data provided"}), resp.BAD_REQUEST_400
    elif data.get('customerNumber'):
        found = session.query(Customer).get(customerNumber_found)
        if found:
            try:
                if data.get('phone'):
                    found.phone = data['phone']
                if data.get('addressLine1'):
                    found.addressLine1 = data['addressLine1']
                if data.get('addressLine2'):
                    found.addressLine2 = data['addressLine2']
                if data.get('postalCode'):
                    found.postalCode = data['postalCode']
                session.add(found)
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


# Create a URL route in our application for "/customers/" to delete an existing row
@customer_routes.route('/customers/<int:customerNumber>', methods=['DELETE'])
def delcustomer(customerNumber):
    customerNumber_found = customerNumber
    found = session.query(Customer).get(customerNumber_found)
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