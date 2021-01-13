#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from api.models.productlines import Productline, ProductlineSchema
from api.utils import responses as resp
from api.utils.database import session
from main import app


@app.route('/productlines/', methods=['GET'])
def allproductlines():
    rows = session.query(Productline).all()
    object_schema = ProductlineSchema(many=True)
    result = object_schema.dump(rows)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


@app.route('/productlines/', methods=['POST'])
def postproductline():
    try:
        data = request.get_json()
        object_schema = ProductlineSchema()
        row = object_schema.load(data)
        session.add(row)
        session.commit()
        result = object_schema.dump(data)
        return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@app.route('/productlines/<string:productLine>', methods=['GET'])
def getproductlines(productLine):
    found = productLine
    row = session.query(Productline).get(found)
    object_schema = ProductlineSchema()
    result = object_schema.dump(row)
    if result:
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200
    else:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404


@app.route('/productlines/<string:productLine>', methods=['PUT'])
def putproductlines(productLine):
    found = productLine
    data = request.get_json()
    object_schema = ProductlineSchema()
    result = object_schema.dump(data)
    try:
        session.query(Productline).filter(Productline.productLine==found).update(result)
        session.commit()
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@app.route('/productlines/<string:productLine>', methods=['DELETE'])
def delproductlines(productLine):
    found = productLine
    try:
        row = session.query(Productline).get(found)
        session.delete(row)
        session.commit()
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    except SQLAlchemyError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400