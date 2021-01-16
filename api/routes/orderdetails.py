#!/usr/bin/python
# -*- coding: utf-8 -*-
""""

"""

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from api.models.orderdetails import Orderdetail, OrderdetailSchema
from api.utils import responses as resp
from api.utils.database import Session


orderdetail_routes = Blueprint("orderdetail_routes", __name__)
object_schema = OrderdetailSchema()
session = Session()


@orderdetail_routes.route('/orderdetails/', methods=['GET'])
def allorderdetails():
    rows = session.query(Orderdetail).all()
    result = object_schema.dump(rows, True)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


@orderdetail_routes.route('/orderdetails/', methods=['POST'])
def postorderdetail():
    try:
        data = request.get_json()           # review datetime
        row = object_schema.load(data)
        session.add(row)
        session.commit()
        result = object_schema.dump(data)
        return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@orderdetail_routes.route('/orderdetails/<int:orderNumber>', methods=['GET'])
def getorderdetails(orderNumber):
    found = orderNumber
    row = session.query(Orderdetail).get(found)
    result = object_schema.dump(row)
    if result:
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200
    else:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404


@orderdetail_routes.route('/orderdetails/<int:orderNumber>', methods=['PUT'])
def putorderdetails(orderNumber):
    found = orderNumber
    data = request.get_json()
    result = object_schema.dump(data)
    try:
        session.query(Orderdetail).filter(Orderdetail.orderNumber==found).update(result)
        session.commit()
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@orderdetail_routes.route('/orderdetails/<int:orderNumber>', methods=['DELETE'])
def delorderdetails(orderNumber):
    found = orderNumber
    try:
        row = session.query(Orderdetail).get(found)
        session.delete(row)
        session.commit()
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    except SQLAlchemyError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400