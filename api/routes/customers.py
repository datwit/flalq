#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from api.models.customers import Customer, CustomerSchema
from api.utils import responses as resp
from api.utils.database import Session


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
    try:
        data = request.get_json()
        row = object_schema.load(data)
        session.add(row)
        session.commit()
        result = object_schema.dump(data)
        return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@customer_routes.route('/customers/<int:customerNumber>', methods=['GET'])
def getcustomer(customerNumber):
    found = customerNumber
    row = session.query(Customer).get(found)
    result = object_schema.dump(row)
    if result:
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200        # "......!!!"
    else:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404


@customer_routes.route('/customers/<int:customerNumber>', methods=['PUT'])
def putcustomer(customerNumber):
    found = customerNumber
    data = request.get_json()
    result = object_schema.dump(data)
    try:
        session.query(Customer).filter(Customer.customerNumber==found).update(result)
        session.commit()
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@customer_routes.route('/customers/<int:customerNumber>', methods=['DELETE'])
def delcustomer(customerNumber):
    found = customerNumber
    try:
        row = session.query(Customer).get(found)
        session.delete(row)
        session.commit()
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    except SQLAlchemyError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400