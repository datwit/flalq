#!/usr/bin/python
# -*- coding: utf-8 -*-
""""

"""

from flask import Blueprint, request
from api.models.orderdetails import Orderdetail, OrderdetailSchema
from api.models.products import Product
from api.utils.database import session, engine
from api.utils import responses as resp
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


orderdetail_routes = Blueprint("orderdetail_routes", __name__)
object_schema = OrderdetailSchema()


@orderdetail_routes.route('/orderdetails/', methods=['GET'])
def allorderdetails():
    rows = session.query(Orderdetail).all()
    result = object_schema.dump(rows, many=True)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


@orderdetail_routes.route('/orderdetails/', methods=['POST'])
def postorderdetail():
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    product_data = data['productCode']
    quantity_data = data['quantityOrdered']
    try:
        row = object_schema.load(data)
        product_ordered = session.query(Product).get(product_data)
        quantity_stock = product_ordered.quantityInStock
        if quantity_data <= quantity_stock:
            row.create()
            quantity_stock = quantity_stock - quantity_data
            product_ordered.quantityInStock = quantity_stock
            session.commit()
            result = object_schema.dump(data)
            return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
        else:
            return resp.response_with(resp.BAD_REQUEST_400, value={"Message": "Not have enough In Stock"}), resp.BAD_REQUEST_400
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@orderdetail_routes.route('/orderdetails/<int:orderNumber>/<int:orderLineNumber>', methods=['GET'])
def getorderdetails(orderNumber, orderLineNumber):
    order_found = orderNumber
    lineNumber_found = orderLineNumber
    row = session.query(Orderdetail).filter(Orderdetail.orderNumber==order_found, Orderdetail.orderLineNumber==lineNumber_found).one()
    if not row:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    else:
        result = object_schema.dump(row)
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200


@orderdetail_routes.route('/orderdetails/<int:orderNumber>/<int:orderLineNumber>', methods=['PATCH'])
def putorderdetails(orderNumber, orderLineNumber):
    order_found = orderNumber
    lineNumber_found = orderLineNumber
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    try:
        if data.get('quantityOrdered'):
            quantity_data = data['quantityOrdered']
            ordered_details = session.query(Orderdetail).filter(Orderdetail.orderNumber==order_found, Orderdetail.orderLineNumber==lineNumber_found).one()
            quantity_before = ordered_details.quantityOrdered
            product_ordered = session.query(Product).get(ordered_details.productCode)
            quantity_stock = product_ordered.quantityInStock
            if quantity_data <= (quantity_stock + quantity_before):
                ordered_details.quantityOrdered = quantity_data
                session.commit()
                quantity_stock = (quantity_stock + quantity_before) - quantity_data
                product_ordered.quantityInStock = quantity_stock
                session.commit()
                result = object_schema.dump(session.query(Orderdetail).filter(Orderdetail.orderNumber==order_found, Orderdetail.orderLineNumber==lineNumber_found).one())
                return resp.response_with(resp.SUCCESS_201, value={"Updated Row": result}), resp.SUCCESS_201
            else:
                return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
        else:
            return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@orderdetail_routes.route('/orderdetails/<int:orderNumber>/<int:orderLineNumber>', methods=['DELETE'])
def delorderdetails(orderNumber, orderLineNumber):
    order_found = orderNumber
    lineNumber_found = orderLineNumber
    try:
        row = session.query(Orderdetail).filter(Orderdetail.orderNumber==order_found, Orderdetail.orderLineNumber==lineNumber_found).one()
        if not row:
            return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
        quantity_product = row.quantityOrdered
        product_found = row.productCode
        session.delete(row)
        session.commit()
        product_ordered = session.query(Product).get(product_found)
        quantity_stock = product_ordered.quantityInStock
        product_ordered.quantityInStock = quantity_stock + quantity_product
        session.commit()
        return resp.response_with(resp.SUCCESS_204, value={'message': 'Deleted Row'}), resp.SUCCESS_204
    except SQLAlchemyError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400