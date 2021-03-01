#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""

from flask import Blueprint, request
from api.models.employees import Employee, EmployeeSchema
from api.utils.database import session, engine
from api.utils import responses as resp
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


employee_routes = Blueprint("employee_routes", __name__)
object_schema = EmployeeSchema()


@employee_routes.route('/employees/', methods=['GET'])
def allemployees():
    rows = session.query(Employee).all()
    result = object_schema.dump(rows, many=True)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


@employee_routes.route('/employees/', methods=['POST'])
def postemployee():
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    try:
        row = object_schema.load(data)
        session.add(row)
        session.commit()
        result = object_schema.dump(session.query(Employee).get(data["employeeNumber"]))
        return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@employee_routes.route('/employees/<int:employeeNumber>', methods=['GET'])
def getemployee(employeeNumber):
    found = employeeNumber
    row = session.query(Employee).get(found)
    if not row:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    else:
        result = object_schema.dump(row)
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200


@employee_routes.route('/employees/<int:employeeNumber>', methods=['PUT'])
def putemployee(employeeNumber):
    found = employeeNumber
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    try:
        row = object_schema.dump(data)
        session.query(Employee).filter(Employee.employeeNumber==found).update(row)
        session.commit()
        result = object_schema.dump(session.query(Employee).get(found))
        return resp.response_with(resp.SUCCESS_201, value={"Updated Row": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@employee_routes.route('/employees/<int:employeeNumber>', methods=['PATCH'])
def patchoffice(employeeNumber):
    found = employeeNumber
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    try:
        row = session.query(Employee).get(found)
        if data.get('extension'):
            row.extension = data['extension']
        if data.get('officeCode'):
            row.officeCode = data['officeCode']
        if data.get('reportsTo'):
            row.reportsTo = data['reportsTo']
        if data.get('jobTitle'):
            row.jobTitle = data['jobTitle']
        session.add(row)
        session.commit()
        result = object_schema.dump(session.query(Employee).get(found))
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row Fields": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400

@employee_routes.route('/employees/<int:employeeNumber>', methods=['DELETE'])
def delemployee(employeeNumber):
    found = employeeNumber
    row = session.query(Employee).get(found)
    if not row:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    try:
        session.delete(row)
        session.commit()
        return resp.response_with(resp.SUCCESS_204, value={'message': 'Deleted Row'}), resp.SUCCESS_204
    except SQLAlchemyError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400