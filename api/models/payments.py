#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import session, Base, engine
from sqlalchemy import  Column, String, Integer, Float, Date, ForeignKey
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from api.models.customers import CustomerSchema


# Payments class
class Payment(Base):
    __tablename__ = "payments"

    customerNumber = Column(Integer, ForeignKey('customers.customerNumber'), primary_key=True,)
    checkNumber = Column(String(50), nullable=False, primary_key=True)
    paymentDate = Column(Date, nullable=False)
    amount = Column(Float(10,2), nullable=False)

    def __init__(self, checkNumber, paymentDate, amount, customerNumber=None):
        self.customerNumber = customerNumber
        self.checkNumber = checkNumber
        self.paymentDate = paymentDate
        self.amount = amount


# Customer schema
class PaymentSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Payment
        sqla_session = session

    customerNumber = fields.Nested(CustomerSchema, many=False, only=['customerNumber'], dump_only=True)
    checkNumber = fields.String(required=True)
    paymentDate = fields.Date(required=True)
    amount = fields.Float(required=True)