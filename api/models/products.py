#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import session, Base, engine
from sqlalchemy import  Column, String, SmallInteger, Integer, DECIMAL, CheckConstraint, ForeignKey, Text, SmallInteger
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from api.models.productlines import ProductlineSchema
from api.models.crudmodel import Crudmodel


# Products class
class Product(Base):
    __tablename__ = "products"

    productCode = Column(String(15), primary_key=True)
    productName = Column(String(70), nullable=False)
    productLine = Column(String(50), ForeignKey('productlines.productLine'), nullable=False)
    productScale = Column(String(10), nullable=False)
    productVendor = Column(String(50), nullable=False)
    productDescription = Column(Text, nullable=False)
    quantityInStock = Column(SmallInteger, nullable=False)
    buyPrice = Column(DECIMAL(10,2), nullable=False)
    MSRP = Column(DECIMAL(10,2), nullable=False)
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
    class Meta(ModelSchema.Meta):
        model = Product
        sqla_session = session

    productCode = fields.String(required=True)
    productName = fields.String(required=True)
    productLine = fields.String(required=True)
    productScale = fields.String(required=True)
    productVendor = fields.String(required=True)
    productDescription = fields.String(required=True)           # marshmallow.fields has not attribute Text
    quantityInStock = fields.Integer(required=True)             # marshmallow.fields has not attribute SmallInteger
    buyPrice = fields.Float(required=True)                      # marshmallow.fields has not attribute DECIMAL
    MSRP = fields.Float(required=True)                          # marshmallow.fields has not attribute DECIMAL