#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from api.models.employees import Employee, EmployeeSchema
from api.utils import responses as resp
from api.utils.database import Session


employee_routes = Blueprint("employee_routes", __name__)
object_schema = EmployeeSchema()
session = Session()


@employee_routes.route('/employees/', methods=['GET'])
def allemployees():
    rows = session.query(Employee).all()
    result = object_schema.dump(rows, many=True)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


@employee_routes.route('/employees/', methods=['POST'])
def postemployee():
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


@employee_routes.route('/employees/<int:employeeNumber>', methods=['GET'])
def getemployee(employeeNumber):
    found = employeeNumber
    row = session.query(Employee).get(found)
    result = object_schema.dump(row)
    if result:
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200
    else:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404


@employee_routes.route('/employees/<int:employeeNumber>', methods=['PUT'])
def putemployee(employeeNumber):
    found = employeeNumber
    data = request.get_json()
    object_schema = EmployeeSchema()
    result = object_schema.dump(data)
    try:
        session.query(Employee).filter(Employee.employeeNumber==found).update(result)
        session.commit()
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@employee_routes.route('/employees/<int:employeeNumber>', methods=['DELETE'])
def delemployee(employeeNumber):
    found = employeeNumber
    try:
        row = session.query(Employee).get(found)
        session.delete(row)
        session.commit()
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    except SQLAlchemyError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400