#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import  ForeignKey, Column, String, Integer, SmallInteger, Float, Date, DateTime, Binary, CheckConstraint
from marshmallow import fields
from sqlalchemy.sql import func
from marshmallow_sqlalchemy import ModelSchema
from api.utils.database import Base, Session


session = Session()


# Productlines class
class Productline(Base):
    __tablename__ = "productlines"

    productLine = Column(String(50), primary_key=True)
    textDescription = Column(String(4000))
    htmlDescription = Column(String(200))                               # validated html format??
    image = Column(Binary)                                              # validate file extension in the path

    def __init__(self, productLine, textDescription, htmlDescription, image):
        self.productLine = productLine
        self.textDescription = textDescription
        self.htmlDescription = htmlDescription
        self.image = image


# Customer schema
class ProductlineSchema(ModelSchema):
    class Meta(ModelSchema.Meta):                                       # "???"
        model = Productline                                             # "???"
        sqla_session = session                                     # "???"

    productLine = fields.String(dump_only=True)
    textDescription = fields.String()
    htmlDescription = fields.String()
    image = fields.String()                                             # path to image