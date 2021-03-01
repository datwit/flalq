#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""

from flask import Blueprint, request, jsonify
from api.models.offices import Office, OfficeSchema
from api.utils.database import session, engine
from api.utils import responses as resp
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


office_routes = Blueprint("office_routes", __name__)
object_schema = OfficeSchema()


# Create a URL route in our application for "/offices/" to read a collection
@office_routes.route('/offices/', methods=['GET'])
def alloffices():
    rows = session.query(Office).all()
    result = object_schema.dump(rows, many=True)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200

# Create a URL route in our application for "/offices/" to create a new row
@office_routes.route('/offices/', methods=['POST'])
def postoffice():
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    try:
        row = object_schema.load(data)
        session.add(row)
        session.commit()
        result = object_schema.dump(session.query(Office).get(data["officeCode"]))
        return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
    except Exception as e:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400

# Create a URL route in our application for "/offices/" to read a particular row in the collection
@office_routes.route('/offices/<string:officeCode>', methods=['GET'])
def getoffice(officeCode):
    found = officeCode
    row = session.query(Office).get(found)
    if not row:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    else:
        result = object_schema.dump(row)
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200
        # return jsonify(result)            # ..OJO...The json response must be like this to test in Postman

# Create a URL route in our application for "/offices/" to update all details of an existing row
@office_routes.route('/offices/<string:officeCode>', methods=['PUT'])
def putoffice(officeCode):
    found = officeCode
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    try:
        row = object_schema.dump(data)
        session.query(Office).filter(Office.officeCode==found).update(row)
        session.commit()
        result = object_schema.dump(session.query(Office).get(found))
        return resp.response_with(resp.SUCCESS_201, value={"Updated Row": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400

# Create a URL route in our application for "/offices/" to update some details of an existing row
@office_routes.route('/offices/<string:officeCode>', methods=['PATCH'])
def patchoffice(officeCode):
    found = officeCode
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    try:
        row = session.query(Office).get(found)
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
        result = object_schema.dump(session.query(Office).get(found))
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row Fields": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400

# Create a URL route in our application for "/offices/" to delete an existing row
@office_routes.route('/offices/<string:officeCode>', methods=['DELETE'])
def deloffice(officeCode):
    found = officeCode
    row = session.query(Office).get(found)
    if not row:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    try:
        session.delete(row)
        session.commit()
        return resp.response_with(resp.SUCCESS_204, value={'message': 'Deleted Row'}), resp.SUCCESS_204     #does not print the message
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400