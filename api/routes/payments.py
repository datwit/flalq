#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from api.models.payments import Payment, PaymentSchema
from api.utils import responses as resp
from api.utils.database import Session


payment_routes = Blueprint("payment_routes", __name__)
object_schema = PaymentSchema()
session = Session()


@payment_routes.route('/payments/', methods=['GET'])
def allpayments():
    rows = session.query(Payment).all()
    result = object_schema.dump(rows, many=True)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


@payment_routes.route('/payments/', methods=['POST'])
def postpayment():
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


@payment_routes.route('/payments/<string:checkNumber>', methods=['GET'])
def getpayments(checkNumber):
    found = checkNumber
    row = session.query(Payment).get(found)
    result = object_schema.dump(row)
    if result:
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200
    else:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404


@payment_routes.route('/payments/<string:checkNumber>', methods=['PUT'])
def putpayments(checkNumber):
    found = checkNumber
    data = request.get_json()
    result = object_schema.dump(data)
    try:
        session.query(Payment).filter(Payment.checkNumber==found).update(result)
        session.commit()
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@payment_routes.route('/payments/<string:checkNumber>', methods=['DELETE'])
def delpayments(checkNumber):
    found = checkNumber
    try:
        row = session.query(Payment).get(found)
        session.delete(row)
        session.commit()
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    except SQLAlchemyError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
