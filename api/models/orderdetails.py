#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import Session, Base
from sqlalchemy import  ForeignKey, Column, String, Integer, SmallInteger, Float, Table
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from api.models.orders import OrderSchema
from api.models.products import ProductSchema


session = Session()


# Orderdetails class
class Orderdetail(Base):
    __tablename__ = "orderdetails"

    orderNumber = Column(Integer, ForeignKey('orders.orderNumber'), primary_key=True)
    productCode = Column(String(15), ForeignKey('products.productCode'), nullable=False, primary_key=True)
    quantityOrdered = Column(Integer, nullable=False)
    priceEach = Column(Float(10,2), nullable=False)
    orderLineNumber = Column(SmallInteger, nullable=False)

    def __init__(self, quantityOrdered, priceEach, orderLineNumber, orderNumber=None, productCode=None):
        self.orderNumber = orderNumber
        self.productCode = productCode
        self.quantityOrdered = quantityOrdered
        self.priceEach = priceEach
        self.orderLineNumber = orderLineNumber


# Customer schema
class OrderdetailSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Orderdetail
        sqla_session = session

    orderNumber = fields.Integer(required=True)
    productCode = fields.String(required=True)
    quantityOrdered = fields.Integer(required=True)
    priceEach = fields.Float(required=True)
    orderLineNumber = fields.Integer(required=True)                     # marchmellow have not SmallInteger fields