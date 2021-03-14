#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import session, Base, engine
from sqlalchemy import  Column, String, Integer, ForeignKey
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


# Employees class
class Employee(Base):
    __tablename__ = "employees"

    employeeNumber = Column(Integer, primary_key=True, autoincrement=False)      # Integer 'Autoincrement' automatically
    lastName = Column(String(50), nullable=False)
    firstName = Column(String(50), nullable=False)
    extension = Column(String(10), nullable=False)
    email = Column(String(100), nullable=False)
    officeCode = Column(String(10), ForeignKey('offices.officeCode'), nullable=False)
    reportsTo = Column(Integer, ForeignKey('employees.employeeNumber'))
    jobTitle = Column(String(50), nullable=False)

    def __init__(self, employeeNumber, lastName, firstName, extension, email, jobTitle, officeCode=None, reportsTo=None):
        self.employeeNumber = employeeNumber
        self.lastName = lastName
        self.firstName = firstName
        self.extension = extension
        self.email = email
        self.officeCode = officeCode
        self.reportsTo = reportsTo
        self.jobTitle = jobTitle


# Employee schema
class EmployeeSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Employee
        sqla_session = session

    employeeNumber = fields.Integer(required=True)
    lastName = fields.String(required=True)
    firstName = fields.String(required=True)
    extension = fields.String(required=True)
    email = fields.String(required=True)
    officeCode = fields.String(required=True)
    reportsTo = fields.Integer()                            # In POST is not required, I suppose because it is 'foreing key'
    jobTitle = fields.String(required=True)