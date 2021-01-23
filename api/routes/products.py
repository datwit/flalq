#!/usr/bin/python
# -*- coding: utf-8 -*-
""""

"""

from flask import Blueprint, request
from api.models.products import Product, ProductSchema
from api.utils.database import Session
from api.utils import responses as resp
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


product_routes = Blueprint("product_routes", __name__)
object_schema = ProductSchema()
session = Session()


@product_routes.route('/products/', methods=['GET'])
def allproducts():
    rows = session.query(Product).all()
    result = object_schema.dump(rows, many=True)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


@product_routes.route('/products/', methods=['POST'])
def postproduct():
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    try:
        row = object_schema.load(data)
        session.add(row)
        session.commit()
        result = object_schema.dump(session.query(Product).get(data["productCode"]))
        return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@product_routes.route('/products/<string:productCode>', methods=['GET'])
def getproducts(productCode):
    found = productCode
    row = session.query(Product).get(found)
    if not row:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    else:
        result = object_schema.dump(row)
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200


@product_routes.route('/products/<string:productCode>', methods=['PUT'])
def putproducts(productCode):
    found = productCode
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    try:
        row = object_schema.dump(data)
        session.query(Product).filter(Product.productCode==found).update(row)
        session.commit()
        result = object_schema.dump(session.query(Product).get(found))
        return resp.response_with(resp.SUCCESS_201, value={"Updated Row": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@product_routes.route('/products/<string:productCode>', methods=['PATCH'])
def patchoffice(productCode):
    found = productCode
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    try:
        row = session.query(Product).get(found)
        if data.get('productVendor'):
            row.productVendor = data['productVendor']
        if data.get('productDescription'):
            row.productDescription = data['productDescription']
        if data.get('buyPrice'):
            row.buyPrice = data['buyPrice']
        session.add(row)
        session.commit()
        result = object_schema.dump(session.query(Product).get(found))
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row Fields": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@product_routes.route('/products/<string:productCode>', methods=['DELETE'])
def delproducts(productCode):
    found = productCode
    row = session.query(Product).get(found)
    if not row:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    try:
        session.delete(row)
        session.commit()
        return resp.response_with(resp.SUCCESS_204, value={'message': 'Deleted Row'}), resp.SUCCESS_204
    except SQLAlchemyError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400