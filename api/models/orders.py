#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import  ForeignKey, Column, String, Integer, SmallInteger, Float, Date, DateTime, Binary, CheckConstraint
from marshmallow import fields
from sqlalchemy.sql import func
from marshmallow_sqlalchemy import ModelSchema
from api.utils.database import Base, Session
from api.models.customers import CustomerSchema


session = Session()


# Orders class
class Order(Base):
    __tablename__ = "orders"

    orderNumber = Column(Integer, primary_key=True)
    orderDate = Column(DateTime, default=func.now(), nullable=False)      # orderDate --> Autocomplete on table in created moment #  #default=datetime.utcnow on_update=datetime.utcnow
    requiredDate = Column(Date, nullable=False)
    shippedDate = Column(Date)
    status = Column(String(15), nullable=False)     # Status field --> this should be like schedule with many options by default, in other table
    comments = Column(String(500))
    customerNumber = Column(Integer, ForeignKey('customers.customerNumber'), nullable=False,)

    def __init__(self, orderNumber, orderDate, requiredDate, shippedDate, status, comments, customerNumber=None):
        self.orderNumber = orderNumber
        self.orderDate = orderDate
        self.requiredDate = requiredDate
        self.shippedDate = shippedDate
        self.status = status
        self.comments = comments
        self.customerNumber = customerNumber


# Customer schema
class OrderSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Order
        sqla_session = session

    orderNumber = fields.Integer(dump_only=True)
    orderDate = fields.Date(dump_only=True)
    requiredDate = fields.Date(required=True)
    shippedDate = fields.Date()
    status = fields.String(required=True)
    comments = fields.String()
    customerNumber = fields.Nested(CustomerSchema, many=False, only=['customerNumber'], required=True)