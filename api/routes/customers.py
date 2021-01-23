#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""

from flask import Blueprint, request
from api.models.customers import Customer, CustomerSchema
from api.utils.database import Session
from api.utils import responses as resp
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


customer_routes = Blueprint("customer_routes", __name__)
object_schema = CustomerSchema()
session = Session()


@customer_routes.route('/customers/', methods=['GET'])
def allcustomers():
    rows = session.query(Customer).all()
    result = object_schema.dump(rows, many=True)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


@customer_routes.route('/customers/', methods=['POST'])
def postcustomer():
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    try:
        row = object_schema.load(data)
        session.add(row)
        session.commit()
        result = object_schema.dump(session.query(Customer).get(data["customerNumber"]))
        return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@customer_routes.route('/customers/<int:customerNumber>', methods=['GET'])
def getcustomer(customerNumber):
    found = customerNumber
    row = session.query(Customer).get(found)
    if not row:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    else:
        result = object_schema.dump(row)
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200


@customer_routes.route('/customers/<int:customerNumber>', methods=['PUT'])
def putcustomer(customerNumber):
    found = customerNumber
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    try:
        row = object_schema.dump(data)
        session.query(Customer).filter(Customer.customerNumber==found).update(row)
        session.commit()
        result = object_schema.dump(session.query(Customer).get(found))
        return resp.response_with(resp.SUCCESS_201, value={"Updated Row": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@customer_routes.route('/customers/<int:customerNumber>', methods=['PATCH'])
def patchoffice(customerNumber):
    found = customerNumber
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    try:
        row = session.query(Customer).get(found)
        if data.get('phone'):
            row.phone = data['phone']
        if data.get('addressLine1'):
            row.addressLine1 = data['addressLine1']
        if data.get('addressLine2'):
            row.addressLine2 = data['addressLine2']
        if data.get('postalCode'):
            row.postalCode = data['postalCode']
        session.add(row)
        session.commit()
        result = object_schema.dump(session.query(Customer).get(found))
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row Fields": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@customer_routes.route('/customers/<int:customerNumber>', methods=['DELETE'])
def delcustomer(customerNumber):
    found = customerNumber
    row = session.query(Customer).get(found)
    if not row:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    try:
        session.delete(row)
        session.commit()
        return resp.response_with(resp.SUCCESS_204, value={'message': 'Deleted Row'}), resp.SUCCESS_204
    except SQLAlchemyError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400