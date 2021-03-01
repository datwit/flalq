#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import session, Base, engine
from sqlalchemy import  ForeignKey, Column, String, Integer, Float, Date, DateTime, Binary
from datetime import datetime
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from api.models.customers import CustomerSchema


# Orders class
class Order(Base):
    __tablename__ = "orders"

    orderNumber = Column(Integer, primary_key=True)
    orderDate = Column(DateTime, default=datetime.now, nullable=False)      # orderDate --> Autocomplete on table in created moment #  #default=datetime.utcnow on_update=datetime.utcnow
    requiredDate = Column(Date, nullable=False)
    shippedDate = Column(Date)
    status = Column(String(15), nullable=False)
    comments = Column(String(500))
    customerNumber = Column(Integer, ForeignKey('customers.customerNumber'), nullable=False)

    def __init__(self, orderNumber, orderDate, requiredDate, shippedDate, status, comments, customerNumber=None):
        self.orderNumber = orderNumber
        self.orderDate = datetime.now()
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

    orderNumber = fields.Integer(required=True)
    orderDate = fields.DateTime()
    requiredDate = fields.Date(required=True)
    shippedDate = fields.Date()
    status = fields.String(required=True)
    comments = fields.String()
    customerNumber = fields.Integer(required=True)