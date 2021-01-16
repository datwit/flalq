#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import  ForeignKey, Column, String, Integer, SmallInteger, Float, Date, DateTime, Binary, CheckConstraint
from marshmallow import fields
from sqlalchemy.sql import func
from marshmallow_sqlalchemy import ModelSchema
from api.utils.database import Base, Session
from api.models.employees import EmployeeSchema


session = Session()


# Customers class
class Customer(Base):
    __tablename__ = "customers"

    customerNumber = Column(Integer, primary_key=True)
    customerName = Column(String(50), nullable=False)
    contactLastName = Column(String(50), nullable=False)
    contactFirstName = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False, unique=True)                     # phone --> I make it unique
    addressLine1 = Column(String(50), nullable=False)
    addressLine2 = Column(String(50))
    city = Column(String(50), nullable=False)
    state = Column(String(50))
    postalCode = Column(String(15))
    country = Column(String(50), nullable=False)
    salesRepEmployeeNumber = Column(Integer, ForeignKey('employees.employeeNumber'))
    creditLimit = Column(Float(10,2))                                       # Float --> because Decimal or Numeric type is not JSON serializable

    def __init__(self, customerNumber, customerName, contactLastName, contactFirstName, phone, addressLine1, addressLine2, city, state, postalCode, country, creditLimit, salesRepEmployeeNumber=None):
        self.customerName = customerNumber
        self.customerName = customerName
        self.contactLastName = contactLastName
        self.contactFirstName = contactFirstName
        self.phone = phone
        self.addressLine1 = addressLine1
        self.addressLine2 = addressLine2
        self.city = city
        self.state = state
        self.postalCode = postalCode
        self.country = country
        self.salesRepEmployeeNumber = salesRepEmployeeNumber
        self.creditLimit = creditLimit


# Customer schema
class CustomerSchema(ModelSchema):
    class Meta(ModelSchema.Meta):                                       # "???"
        model = Customer                                                # "???"
        sqla_session = session                                          # "???"

    customerNumber = fields.Integer(dump_only=True)
    customerName = fields.String(required=True)
    contactLastName = fields.String(required=True)
    contactFirstName = fields.String(required=True)
    phone = fields.String(required=True)
    addressLine1 = fields.String(required=True)
    addressLine2 = fields.String()
    city = fields.String(required=True)
    state = fields.String()
    postalCode = fields.String()
    country = fields.String(required=True)
    salesRepEmployeeNumber = fields.Nested(EmployeeSchema, many=True, only=['employeeNumber'])
    creditLimit = fields.Float()