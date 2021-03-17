#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""

from flask import Blueprint, request
from api.models.payments import Payment, PaymentSchema
from api.utils.database import session, engine
from api.utils import responses as resp
from sqlalchemy import text


payment_routes = Blueprint("payment_routes", __name__)
object_schema = PaymentSchema()

# Create a URL route in our application for "/payments/" to read a collection
@payment_routes.route('/payments/', methods=['GET'])
def allpayments():
    rows = session.query(Payment).all()
    result = object_schema.dump(rows, many=True)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


# Create a URL route in our application for "/payments/" to create a new row
@payment_routes.route('/payments/', methods=['POST'])
def postpayment():
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "No input data provided"}), resp.BAD_REQUEST_400
    elif data.get('customerNumber') and data.get('checkNumber'):
        found = session.query(Payment).get({"customerNumber": data["customerNumber"], "checkNumber": data["checkNumber"]})
        if not found:
            try:
                row = object_schema.load(data)
                session.add(row)
                session.commit()
                result = object_schema.dump(session.query(Payment).get({"customerNumber": data["customerNumber"], "checkNumber": data["checkNumber"]}))
                return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
            except Exception as e:
                session.rollback()
                return resp.response_with(resp.BAD_REQUEST_400, value={"error": str(e)}), resp.BAD_REQUEST_400
        else:
            return resp.response_with(resp.INVALID_FIELD_NAME_SENT_422, value={"error": "Key data already exists"}), resp.INVALID_FIELD_NAME_SENT_422
    else:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "Data no has key field"}), resp.BAD_REQUEST_400


# Create a URL route in our application for "/payments/" to read a particular row in the collection
@payment_routes.route('/payments/<string:customerNumber>/<string:checkNumber>', methods=['GET'])
def getpayments(customerNumber, checkNumber):
    customerNumber_found = customerNumber
    checkNumber_found = checkNumber
    found = session.query(Payment).get({"customerNumber": customerNumber_found, "checkNumber": checkNumber_found})
    if not found:
        return resp.response_with(resp.SERVER_ERROR_404, value={"error": "The request data no exists"}), resp.SERVER_ERROR_404
    else:
        result = object_schema.dump(found)
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200


# Create a URL route in our application for "/payments/" to update all details of an existing row
@payment_routes.route('/payments/<string:customerNumber>/<string:checkNumber>', methods=['PUT'])
def putpayments(customerNumber, checkNumber):
    customerNumber_found = customerNumber
    checkNumber_found = checkNumber
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "No input data provided"}), resp.BAD_REQUEST_400
    elif data.get('customerNumber') and data.get('checkNumber'):
        found = session.query(Payment).get({"customerNumber": customerNumber_found, "checkNumber": checkNumber_found})
        if found:
            try:
                row = object_schema.load(data)
                if row:
                    session.query(Payment).filter(Payment.customerNumber==customerNumber_found, Payment.checkNumber==checkNumber_found).update(data)
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


# Create a URL route in our application for "/payments/" to delete an existing row
@payment_routes.route('/payments/<string:customerNumber>/<string:checkNumber>', methods=['DELETE'])
def delpayments(customerNumber, checkNumber):
    customerNumber_found = customerNumber
    checkNumber_found = checkNumber
    found = session.query(Payment).get({"customerNumber": customerNumber_found, "checkNumber": checkNumber_found})
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