#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import  ForeignKey, Column, String, Integer, SmallInteger, Float, Date, DateTime, Binary, CheckConstraint
from marshmallow import fields
from sqlalchemy.sql import func
from marshmallow_sqlalchemy import ModelSchema
from api.utils.database import Base, session
from api.models.offices import OfficeSchema


# Employees class
class Employee(Base):
    __tablename__ = "employees"

    employeeNumber = Column(Integer, primary_key=True)        # Integer and primary_key is auto-incremented automatically in table structure
    lastName = Column(String(50), nullable=False)
    firstName = Column(String(50), nullable=False)
    extension = Column(String(10), nullable=False)
    email = Column(String(100), nullable=False, unique=True)                  # email --> I make it unique
    officeCode = Column(String(10), ForeignKey('offices.officeCode'), nullable=False,)
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

    def create(self):
        session.add(self)
        session.commit()
        return self

# Employee schema
class EmployeeSchema(ModelSchema):
    class Meta(ModelSchema.Meta):                                      # "???"
        model = Employee                                               # "???"
        sqla_session = session                                         # "???"

    employeeNumber = fields.Integer(dump_only=True)
    lastName = fields.String(required=True)
    firstName = fields.String(required=True)
    extension = fields.String(required=True)
    email = fields.String(required=True)                               # validate email format
    officeCode = fields.Nested(OfficeSchema, many=False, only=['officeCode'], required=True)
    reportsTo = fields.Integer()
    jobTitle = fields.String(required=True)