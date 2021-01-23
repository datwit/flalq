#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""

from flask import Blueprint, request
from api.models.productlines import Productline, ProductlineSchema
from api.utils.database import Session
from api.utils import responses as resp
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


productline_routes = Blueprint("productline_routes", __name__)
object_schema = ProductlineSchema()
session = Session()


@productline_routes.route('/productlines/', methods=['GET'])
def allproductlines():
    rows = session.query(Productline).all()
    result = object_schema.dump(rows, many=True)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


@productline_routes.route('/productlines/', methods=['POST'])
def postproductline():
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    try:
        row = object_schema.load(data)
        session.add(row)
        session.commit()
        result = object_schema.dump(session.query(Productline).get(data["productLine"]))
        return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@productline_routes.route('/productlines/<string:productLine>', methods=['GET'])
def getproductlines(productLine):
    found = productLine
    row = session.query(Productline).get(found)
    if not row:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    else:
        result = object_schema.dump(row)
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200


@productline_routes.route('/productlines/<string:productLine>', methods=['PUT'])
def putproductlines(productLine):
    found = productLine
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    try:
        row = object_schema.dump(data)
        session.query(Productline).filter(Productline.productLine==found).update(row)
        session.commit()
        result = object_schema.dump(session.query(Productline).get(found))
        return resp.response_with(resp.SUCCESS_201, value={"Updated Row": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@productline_routes.route('/productlines/<string:productLine>', methods=['PATCH'])
def patchoffice(productLine):
    found = productLine
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    try:
        row = session.query(Productline).get(found)
        if data.get('textDescription'):
            row.textDescription = data['textDescription']
        if data.get('htmlDescription'):
            row.htmlDescription = data['htmlDescription']
        if data.get('image'):
            row.image = data['image']
        session.add(row)
        session.commit()
        result = object_schema.dump(session.query(Productline).get(found))
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row Fields": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@productline_routes.route('/productlines/<string:productLine>', methods=['DELETE'])
def delproductlines(productLine):
    found = productLine
    row = session.query(Productline).get(found)
    if not row:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    try:
        session.delete(row)
        session.commit()
        return resp.response_with(resp.SUCCESS_204, value={'message': 'Deleted Row'}), resp.SUCCESS_204
    except SQLAlchemyError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400