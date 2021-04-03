#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import session, Base, engine
from sqlalchemy import Column, Integer, ForeignKey, String, DECIMAL, SmallInteger
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from api.models.orders import OrderSchema
from api.models.products import ProductSchema


# Orderdetails class
class Orderdetail(Base):
    __tablename__ = "orderdetails"

    orderNumber = Column(Integer, ForeignKey('orders.orderNumber'), primary_key=True)
    productCode = Column(String(15), ForeignKey('products.productCode'), nullable=False, primary_key=True)
    quantityOrdered = Column(Integer, nullable=False)
    priceEach = Column(DECIMAL(10,2), nullable=False)
    orderLineNumber = Column(SmallInteger(), nullable=False)

    def __init__(self, quantityOrdered, priceEach, orderLineNumber, orderNumber=None, productCode=None):
        self.orderNumber = orderNumber
        self.productCode = productCode
        self.quantityOrdered = quantityOrdered
        self.priceEach = priceEach
        self.orderLineNumber = orderLineNumber

    def create(self):
        session.add(self)
        session.commit()
        return self


# Customer schema
class OrderdetailSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Orderdetail
        sqla_session = session

    orderNumber = fields.Integer(required=True)
    productCode = fields.String(required=True)
    quantityOrdered = fields.Integer(required=True)
    priceEach = fields.Float(required=True)                     # marshmallow.fields has not attribute DECIMAL
    orderLineNumber = fields.Integer(required=True)             # marshmallow.fields has not attribute SmallInteger