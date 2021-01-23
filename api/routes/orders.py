#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""

from flask import Blueprint, request
from api.models.orders import Order, OrderSchema
from api.utils.database import Session
from api.utils import responses as resp
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

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
    data = request.get_json()           # review datetime, quantity in stock
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    try:
        row = object_schema.load(data)
        session.add(row)
        session.commit()
        result = object_schema.dump(session.query(Order).get(data["orderNumber"]))
        return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@order_routes.route('/orders/<int:orderNumber>', methods=['GET'])
def getorders(orderNumber):
    found = orderNumber
    row = session.query(Order).get(found)
    if not row:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    else:
        result = object_schema.dump(row)
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200


@order_routes.route('/orders/<int:orderNumber>', methods=['PUT'])
def putorders(orderNumber):
    found = orderNumber
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    try:
        row = object_schema.dump(data)
        session.query(Order).filter(Order.orderNumber==found).update(row)
        session.commit()
        result = object_schema.dump(session.query(Order).get(found))
        return resp.response_with(resp.SUCCESS_201, value={"Updated Row": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@order_routes.route('/orders/<int:orderNumber>', methods=['PATCH'])
def patchoffice(orderNumber):
    found = orderNumber
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    try:
        row = session.query(Order).get(found)
        if data.get('requiredDate'):
            row.requiredDate = data['requiredDate']
        if data.get('shippedDate'):
            row.shippedDate = data['shippedDate']
        if data.get('status'):
            row.status = data['status']
        if data.get('comments'):
            row.comments = data['comments']
        session.add(row)
        session.commit()
        result = object_schema.dump(session.query(Order).get(found))
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row Fields": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@order_routes.route('/orders/<int:orderNumber>', methods=['DELETE'])
def delorders(orderNumber):
    found = orderNumber
    row = session.query(Order).get(found)
    if not row:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    try:
        session.delete(row)
        session.commit()
        return resp.response_with(resp.SUCCESS_204, value={'message': 'Deleted Row'}), resp.SUCCESS_204
    except SQLAlchemyError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400