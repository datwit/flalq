#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""

from flask import Blueprint, request, jsonify
from api.models.offices import Office, OfficeSchema
from api.utils.database import session, engine
from api.utils import responses as resp
from sqlalchemy import text


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
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "No input data provided"}), resp.BAD_REQUEST_400
    elif data.get('officeCode'):
        found = session.query(Office).get(data["officeCode"])
        if not found:
            try:
                row = object_schema.load(data)
                session.add(row)
                session.commit()
                result = object_schema.dump(session.query(Office).get(data["officeCode"]))
                return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
            except Exception as e:
                session.rollback()
                return resp.response_with(resp.BAD_REQUEST_400, value={"error": str(e)}), resp.BAD_REQUEST_400
        else:
            return resp.response_with(resp.INVALID_FIELD_NAME_SENT_422, value={"error": "Key data already exists"}), resp.INVALID_FIELD_NAME_SENT_422
    else:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "Data no has key field"}), resp.BAD_REQUEST_400


# Create a URL route in our application for "/offices/" to read a particular row in the collection
@office_routes.route('/offices/<string:officeCode>', methods=['GET'])
def getoffice(officeCode):
    officeCode_found = officeCode
    found = session.query(Office).get(officeCode_found)
    if not found:
        return resp.response_with(resp.SERVER_ERROR_404, value={"error": "The request data no exists"}), resp.SERVER_ERROR_404
    else:
        result = object_schema.dump(found)
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200
        # return jsonify(result)            # ..OJO...The json response must be like this to test in Postman


# Create a URL route in our application for "/offices/" to update all details of an existing row
@office_routes.route('/offices/<string:officeCode>', methods=['PUT'])
def putoffice(officeCode):
    officeCode_found = officeCode
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "No input data provided"}), resp.BAD_REQUEST_400
    elif data.get('officeCode'):
        found = session.query(Office).get(officeCode_found)
        if found:
            try:
                row = object_schema.dump(data)
                session.query(Office).filter(Office.officeCode==officeCode_found).update(row)
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


# Create a URL route in our application for "/offices/" to update some details of an existing row
@office_routes.route('/offices/<string:officeCode>', methods=['PATCH'])
def patchoffice(officeCode):
    officeCode_found = officeCode
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "No input data provided"}), resp.BAD_REQUEST_400
    elif data.get('officeCode'):
        found = session.query(Office).get(officeCode_found)
        if found:
            try:
                if data.get('phone'):
                    found.phone = data['phone']
                if data.get('postalCode'):
                    found.postalCode = data['postalCode']
                if data.get('addressLine1'):
                    found.addressLine1 = data['addressLine1']
                if data.get('addressLine2'):
                    found.addressLine2 = data['addressLine2']
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


# Create a URL route in our application for "/offices/" to delete an existing row
@office_routes.route('/offices/<string:officeCode>', methods=['DELETE'])
def deloffice(officeCode):
    officeCode_found = officeCode
    found = session.query(Office).get(officeCode_found)
    if found:
        try:
            session.delete(found)
            session.commit()
            return resp.response_with(resp.SUCCESS_204, value={'message': 'Deleted Row'}), resp.SUCCESS_204     #does not print the message
        except Exception as e:
            session.rollback()
            return resp.response_with(resp.BAD_REQUEST_400, value={"error": str(e)}), resp.BAD_REQUEST_400
    else:
        return resp.response_with(resp.SERVER_ERROR_404, value={"error": "The request data no exists"}), resp.SERVER_ERROR_404