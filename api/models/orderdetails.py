#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import  ForeignKey, Column, String, Integer, SmallInteger, Float, Table
from sqlalchemy.orm import relationship
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from api.utils.database import Base, Session
from api.models.orders import OrderSchema
from api.models.products import ProductSchema


session = Session()

association_table = Table('association', Base.metadata,
    Column('orderdetail_productCode', String, ForeignKey('orderdetail.productCode')),
    Column('product_productCode', String, ForeignKey('product.productCode'))
)


# Orderdetails class
class Orderdetail(Base):
    __tablename__ = "orderdetails"

    orderNumber = Column(Integer, ForeignKey('orders.orderNumber'), primary_key=True)
    productCode = Column(String(15), ForeignKey('products.productCode'), nullable=False, primary_key=True)
    quantityOrdered = Column(Integer, nullable=False)
    priceEach = Column(Float(10,2), nullable=False)
    orderLineNumber = Column(SmallInteger, nullable=False)
    products = relationship("Product", secondary=association_table, backref="Order")

    def __init__(self, quantityInStock, priceEach, orderLineNumber, orderNumber=None, productCode=None):
        self.orderNumber = orderNumber
        self.productCode = productCode
        self.quantityOrdered = quantityInStock
        self.priceEach = priceEach
        self.orderLineNumber = orderLineNumber


# Customer schema
class OrderdetailSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Orderdetail
        sqla_session = session

    orderNumber = fields.Nested(OrderSchema, many=False, only=['orderNumber'], dump_only=True)
    productCode = fields.Nested(ProductSchema, many=False, only=['productCode'], required=True)
    quantityOrdered = fields.Integer(required=True)
    priceEach = fields.Float(required=True)
    orderLineNumber = fields.Integer(required=True)                     # marchmellow have not SmallInteger fields