#!/usr/bin/python
# -*- coding: utf-8 -*-
""""

"""

from flask import Blueprint, request
from api.models.orderdetails import Orderdetail, OrderdetailSchema
from api.models.products import Product
from api.utils.database import Session
from api.utils import responses as resp
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


orderdetail_routes = Blueprint("orderdetail_routes", __name__)
object_schema = OrderdetailSchema()
session = Session()


@orderdetail_routes.route('/orderdetails/', methods=['GET'])
def allorderdetails():
    rows = session.query(Orderdetail).all()
    result = object_schema.dump(rows, many=True)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


@orderdetail_routes.route('/orderdetails/', methods=['POST'])
def postorderdetail():
    data = request.get_json()
    productCode = data['productCode']
    orderNumber = data['orderNumber']
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    try:
        row = object_schema.load(data)
        ordered_product = session.query(Product).get(productCode)
        if ordered_product['quantityInStock'] > data['quantityOrdered']:
            session.add(row)
            session.commit()
            ordered_product['quantityInStock'] = ordered_product['quantityInStock'] - row['quantityOrdered']
            session.add(ordered_product)
            session.commit()
            result = object_schema.dump(session.query(Orderdetail).get(orderNumber))
            return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
        else:
            return resp.response_with(resp.BAD_REQUEST_400, value={"Message": "Not have enough In Stock"}), resp.BAD_REQUEST_400
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@orderdetail_routes.route('/orderdetails/<int:orderNumber>', methods=['GET'])
def getorderdetails(orderNumber):
    found = orderNumber
    row = session.query(Orderdetail).get(found)
    if not row:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    else:
        result = object_schema.dump(row)
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200


@orderdetail_routes.route('/orderdetails/<int:orderNumber>', methods=['PUT'])
def putorderdetails(orderNumber):
    found = orderNumber
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    try:
        row = object_schema.dump(data)
        ordered_product = session.query(Product).get(row['productCode'])
        ordered_product.quantityInStock = ordered_product['quantityInStock'] + row['quantityOrdered']
        if ordered_product['quantityInStock'] >= row['quantityOrdered']:
            session.query(Orderdetail).filter(Orderdetail.orderNumber==found).update(row)
            session.commit()
            ordered_product.quantityInStock = ordered_product['quantityInStock'] - row['quantityOrdered']
            session.add(ordered_product)
            session.commit()
            result = object_schema.dump(session.query(Orderdetail).get(found))
            return resp.response_with(resp.SUCCESS_201, value={"Updated Row": result}), resp.SUCCESS_201
        else:
            return resp.response_with(resp.BAD_REQUEST_400, value={"Message": "Not have enough In Stock"}), resp.BAD_REQUEST_400
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@orderdetail_routes.route('/orderdetails/<int:orderNumber>', methods=['PATCH'])
def patchoffice(orderNumber):
    found = orderNumber
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    try:
        row = session.query(Orderdetail).get(found)
        if data.get('quantityOrdered'):
            ordered_product = session.query(Product).get(row['productCode'])
            ordered_product.quantityInStock = ordered_product['quantityInStock'] + row['quantityOrdered']
            if ordered_product['quantityInStock'] >= data['quantityOrdered']:
                row.quantityOrdered = data['quantityOrdered']
                session.add(row)
                session.commit()
                ordered_product.quantityInStock = ordered_product['quantityInStock'] - row['quantityOrdered']
                session.add(ordered_product)
                session.commit()
                result = object_schema.dump(row)
                return resp.response_with(resp.SUCCESS_200, value={"Updated Row Fields": result}), resp.SUCCESS_200
            else:
                return resp.response_with(resp.BAD_REQUEST_400, value={"Message": "Not have enough In Stock"}), resp.BAD_REQUEST_400
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@orderdetail_routes.route('/orderdetails/<int:orderNumber>', methods=['DELETE'])
def delorderdetails(orderNumber):
    found = orderNumber
    row = session.query(Orderdetail).get(found)
    if not row:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    try:
        session.delete(row)
        session.commit()
        return resp.response_with(resp.SUCCESS_204, value={'message': 'Deleted Row'}), resp.SUCCESS_204
    except SQLAlchemyError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400