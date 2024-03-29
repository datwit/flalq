#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""

from flask import Blueprint, request
from api.models.employees import Employee, EmployeeSchema
from api.utils.database import session, engine
from api.utils import responses as resp
from sqlalchemy import text


employee_routes = Blueprint("employee_routes", __name__)
object_schema = EmployeeSchema()

# Create a URL route in our application for "/employees/" to read a collection
@employee_routes.route('/employees/', methods=['GET'])
def allemployees():
    rows = session.query(Employee).all()
    result = object_schema.dump(rows, many=True)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


# Create a URL route in our application for "/employees/" to create a new row
@employee_routes.route('/employees/', methods=['POST'])
def postemployee():
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "No input data provided"}), resp.BAD_REQUEST_400
    elif data.get('employeeNumber'):
        found = session.query(Employee).get(data["employeeNumber"])
        if not found:
            try:
                row = object_schema.load(data)
                session.add(row)
                session.commit()
                result = object_schema.dump(session.query(Employee).get(data["employeeNumber"]))
                return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
            except Exception as e:
                session.rollback()
                return resp.response_with(resp.BAD_REQUEST_400, value={"error": str(e)}), resp.BAD_REQUEST_400
        else:
            return resp.response_with(resp.INVALID_FIELD_NAME_SENT_422, value={"error": "Key data already exists"}), resp.INVALID_FIELD_NAME_SENT_422
    else:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "Data no has key field"}), resp.BAD_REQUEST_400


# Create a URL route in our application for "/employees/" to read a particular row in the collection
@employee_routes.route('/employees/<int:employeeNumber>', methods=['GET'])
def getemployee(employeeNumber):
    employeeNumber_found = employeeNumber
    found = session.query(Employee).get(employeeNumber_found)
    if not found:
        return resp.response_with(resp.SERVER_ERROR_404, value={"error": "The request data no exists"}), resp.SERVER_ERROR_404
    else:
        result = object_schema.dump(found)
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200


# Create a URL route in our application for "/employees/" to update all details of an existing row
@employee_routes.route('/employees/<int:employeeNumber>', methods=['PUT'])
def putemployee(employeeNumber):
    employeeNumber_found = employeeNumber
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "No input data provided"}), resp.BAD_REQUEST_400
    elif data.get('employeeNumber'):
        found = session.query(Employee).get(employeeNumber_found)
        if found:
            try:
                row = object_schema.dump(data)
                session.query(Employee).filter(Employee.employeeNumber==employeeNumber_found).update(row)
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


# Create a URL route in our application for "/employee/" to update some details of an existing row
@employee_routes.route('/employees/<int:employeeNumber>', methods=['PATCH'])
def patchoffice(employeeNumber):
    employeeNumber_found = employeeNumber
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "No input data provided"}), resp.BAD_REQUEST_400
    elif data.get('employeeNumber'):
        found = session.query(Employee).get(employeeNumber_found)
        if found:
            try:
                if data.get('extension'):
                    found.extension = data['extension']
                if data.get('officeCode'):
                    found.officeCode = data['officeCode']
                if data.get('reportsTo'):
                    found.reportsTo = data['reportsTo']
                if data.get('jobTitle'):
                    found.jobTitle = data['jobTitle']
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


# Create a URL route in our application for "/employees/" to delete an existing row
@employee_routes.route('/employees/<int:employeeNumber>', methods=['DELETE'])
def delemployee(employeeNumber):
    employeeNumber_found = employeeNumber
    found = session.query(Employee).get(employeeNumber_found)
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