#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from api.models.orders import Order, OrderSchema
from api.utils import responses as resp
from api.utils.database import Session

order_routes = Blueprint("order_routes", __name__)
object_schema = OrderSchema()
session = Session()


@order_routes.route('/orders/', methods=['GET'])
def allorders():
    rows = session.query(Order).all()
    result = object_schema.dump(rows, many=True)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


@order_routes.route('/orders/', methods=['POST'])
def postorder():
    try:
        data = request.get_json()           # review datetime, quantity in stock
        row = object_schema.load(data)
        session.add(row)
        session.commit()
        result = object_schema.dump(data)
        return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@order_routes.route('/orders/<int:orderNumber>', methods=['GET'])
def getorders(orderNumber):
    found = orderNumber
    row = session.query(Order).get(found)
    result = object_schema.dump(row)
    if result:
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200
    else:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404


@order_routes.route('/orders/<int:orderNumber>', methods=['PUT'])
def putorders(orderNumber):
    found = orderNumber
    data = request.get_json()
    result = object_schema.dump(data)
    try:
        session.query(Order).filter(Order.orderNumber==found).update(result)
        session.commit()
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@order_routes.route('/orders/<int:orderNumber>', methods=['DELETE'])
def delorders(orderNumber):
    found = orderNumber
    try:
        row = session.query(Order).get(found)
        session.delete(row)
        session.commit()
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    except SQLAlchemyError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400