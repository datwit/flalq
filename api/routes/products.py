#!/usr/bin/python
# -*- coding: utf-8 -*-
""""

"""

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from api.models.products import Product, ProductSchema
from api.utils import responses as resp
from api.utils.database import Session


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


@product_routes.route('/products/<string:productCode>', methods=['GET'])
def getproducts(productCode):
    found = productCode
    row = session.query(Product).get(found)
    result = object_schema.dump(row)
    if result:
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200
    else:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404


@product_routes.route('/products/<string:productCode>', methods=['PUT'])
def putproducts(productCode):
    found = productCode
    data = request.get_json()
    result = object_schema.dump(data)
    try:
        session.query(Product).filter(Product.productCode==found).update(result)
        session.commit()
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400

@product_routes.route('/products/<string:productCode>', methods=['DELETE'])
def delproducts(productCode):
    found = productCode
    try:
        row = session.query(Product).get(found)
        session.delete(row)
        session.commit()
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    except SQLAlchemyError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400