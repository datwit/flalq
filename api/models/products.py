#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import  ForeignKey, Column, String, Integer, SmallInteger, Float, Date, DateTime, Binary, CheckConstraint
from marshmallow import fields
from sqlalchemy.sql import func
from marshmallow_sqlalchemy import ModelSchema
from api.utils.database import Base, Session
from api.models.productlines import ProductlineSchema


session = Session()


# Products class
class Product(Base):
    __tablename__ = "products"

    productCode = Column(String(15), primary_key=True)
    productName = Column(String(70), nullable=False)
    productLine = Column(String(50), ForeignKey('productlines.productLine'), nullable=False)
    productScale = Column(String(10), nullable=False)
    productVendor = Column(String(50), nullable=False)
    productDescription = Column(String(500), nullable=False)
    quantityInStock = Column(SmallInteger, nullable=False)
    buyPrice = Column(Float(10,2), nullable=False)
    MSRP = Column(Float(10,2), nullable=False)
    CheckConstraint('quantityInStock >= 0', name='quantityInStock_positive')        # I am ensuring that quantityInStock data is always positive

    def __init__(self, productCode, productName, productScale, productVendor, productDescription, quantityInStock, buyPrice, MSRP, productLine=None):
        self.productCode = productCode
        self.productName = productName
        self.productLine = productLine
        self.productScale = productScale
        self.productVendor = productVendor
        self.productDescription = productDescription
        self.quantityInStock = quantityInStock
        self.buyPrice = buyPrice
        self.MSRP = MSRP


# Customer schema
class ProductSchema(ModelSchema):
    class Meta(ModelSchema.Meta):                                       # "???"
        model = Product                                                 # "???"
        sqla_session = session                                          # "???"

    productCode = fields.String(dump_only=True)
    productName = fields.String(required=True)
    productLine = fields.Nested(ProductlineSchema, many=False, only=['productLine'], required=True)
    productScale = fields.String(required=True)
    productVendor = fields.String(required=True)
    productDescription = fields.String(required=True)
    quantityInStock = fields.Integer(required=True)                     # marchmellow have not SmallInteger fields
    buyPrice = fields.Float(required=True)
    MSRP = fields.Float(required=True)