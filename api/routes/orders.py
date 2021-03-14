#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""

from flask import Blueprint, request
from api.models.orders import Order, OrderSchema
from api.utils.database import session, engine
from api.utils import responses as resp
from sqlalchemy import text


order_routes = Blueprint("order_routes", __name__)
object_schema = OrderSchema()

# Create a URL route in our application for "/orders/" to read a collection
@order_routes.route('/orders/', methods=['GET'])
def allorders():
    rows = session.query(Order).all()
    result = object_schema.dump(rows, many=True)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


# Create a URL route in our application for "/orders/" to create a new row
@order_routes.route('/orders/', methods=['POST'])
def postorder():
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "No input data provided"}), resp.BAD_REQUEST_400
    elif data.get('orderNumber'):
        found = session.query(Order).get(data["orderNumber"])
        if not found:
            try:
                row = object_schema.load(data)
                session.add(row)
                session.commit()
                result = object_schema.dump(session.query(Order).get(data["orderNumber"]))
                return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
            except Exception as e:
                session.rollback()
                return resp.response_with(resp.BAD_REQUEST_400, value={"error": str(e)}), resp.BAD_REQUEST_400
        else:
            return resp.response_with(resp.INVALID_FIELD_NAME_SENT_422, value={"error": "Key data already exists"}), resp.INVALID_FIELD_NAME_SENT_422
    else:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "Data no has key field"}), resp.BAD_REQUEST_400


# Create a URL route in our application for "/orderNumber/" to read a particular row in the collection
@order_routes.route('/orders/<int:orderNumber>', methods=['GET'])
def getorders(orderNumber):
    orderNumber_found = orderNumber
    found = session.query(Order).get(orderNumber_found)
    if not found:
        return resp.response_with(resp.SERVER_ERROR_404, value={"error": "The request data no exists"}), resp.SERVER_ERROR_404
    else:
        result = object_schema.dump(found)
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200


# Create a URL route in our application for "/orders/" to update all details of an existing row
@order_routes.route('/orders/<int:orderNumber>', methods=['PUT'])
def putorders(orderNumber):
    orderNumber_found = orderNumber
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "No input data provided"}), resp.BAD_REQUEST_400
    elif data.get('orderNumber'):
        found = session.query(Order).get(orderNumber_found)
        if found:
            try:
                row = object_schema.dump(data)
                session.query(Order).filter(Order.orderNumber==orderNumber_found).update(row)
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


# Create a URL route in our application for "/orders/" to update some details of an existing row
@order_routes.route('/orders/<int:orderNumber>', methods=['PATCH'])
def patchoffice(orderNumber):
    ordersNumber_found = orderNumber
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "No input data provided"}), resp.BAD_REQUEST_400
    elif data.get('ordersNumber'):
        found = session.query(Order).get(ordersNumber_found)
        if found:
            try:
                if data.get('requiredDate'):
                    found.requiredDate = data['requiredDate']
                if data.get('shippedDate'):
                    found.shippedDate = data['shippedDate']
                if data.get('status'):
                    found.status = data['status']
                if data.get('comments'):
                    found.comments = data['comments']
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


# Create a URL route in our application for "/orders/" to delete an existing row
@order_routes.route('/orders/<int:orderNumber>', methods=['DELETE'])
def delorders(orderNumber):
    orderNumber_found = orderNumber
    found = session.query(Order).get(orderNumber_found)
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