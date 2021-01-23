#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import Session, Base
from sqlalchemy import Column, String, Binary
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


session = Session()


# Productlines class
class Productline(Base):
    __tablename__ = "productlines"

    productLine = Column(String(50), primary_key=True)
    textDescription = Column(String(4000))
    htmlDescription = Column(String(200))                               # validated html format??
    image = Column(String(100))                                         # validate file extension in the path

    def __init__(self, productLine, textDescription, htmlDescription, image):
        self.productLine = productLine
        self.textDescription = textDescription
        self.htmlDescription = htmlDescription
        self.image = image


# Customer schema
class ProductlineSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Productline
        sqla_session = session

    productLine = fields.String(required=True)
    textDescription = fields.String()
    htmlDescription = fields.String()
    image = fields.String()                                             # path to image