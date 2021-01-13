#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from api.models.offices import Office, OfficeSchema
from api.utils import responses as resp
from api.utils.database import session
from main import app


# Create a URL route in our application for "/offices/" to read a collection
@app.route('/offices/', methods=['GET'])
def alloffices():
    rows = session.query(Office).order_by(Office.state).all()           # Using order_by to see how work this
    object_schema = OfficeSchema(many=True)
    result = object_schema.dump(rows)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200        # I did many way for this resp. *.bmp

# Create a URL route in our application for "/offices/" to create a new row
@app.route('/offices/', methods=['POST'])
def postoffice():
    try:
        data = request.get_json()
        object_schema = OfficeSchema()
        row = object_schema.load(data)
        session.add(row)
        session.commit()
        result = object_schema.dump(data)
        return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400   # 422 ó 400 ... ???

# Create a URL route in our application for "/offices/" to read a particular row in the collection
@app.route('/offices/<string:officeCode>', methods=['GET'])
def getoffice(officeCode):
    found = officeCode
    row = session.query(Office).get(found)
    object_schema = OfficeSchema()
    result = object_schema.dump(row)
    if result:
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200
    else:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404

# Create a URL route in our application for "/offices/" to update all details of an existing row
@app.route('/offices/<string:officeCode>', methods=['PUT'])
def putoffice(officeCode):
    found = officeCode
    data = request.get_json()
    object_schema = OfficeSchema()
    result = object_schema.dump(data)
    try:
        session.query(Office).filter(Office.officeCode==found).update(result)
        session.commit()
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400

# Create a URL route in our application for "/offices/" to update some details of an existing row
@app.route('/offices/<string:officeCode>', methods=['PATCH'])
def patchoffice(officeCode):
    found = officeCode
    data = request.get_json()
    row = session.query(Office).get(found)
    try:
        if data.get('phone'):
            row.phone = data['phone']
        if data.get('postalCode'):
            row.postalCode = data['postalCode']
        if data.get('addressLine1'):
            row.addressLine1 = data['addressLine1']
        if data.get('addressLine2'):
            row.addressLine2 = data['addressLine2']
        session.add(row)
        session.commit()
        object_schema = OfficeSchema()
        result = object_schema.dump(row)
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row Fields": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400

# Create a URL route in our application for "/offices/" to delete an existing row
@app.route('/offices/<string:officeCode>', methods=['DELETE'])
def deloffice(officeCode):
    found = officeCode
    try:
        row = session.query(Office).get(found)
        session.delete(row)
        session.commit()
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    except SQLAlchemyError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400       #or 204??