#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Class to Offices Table and Office Schema
"""

from api.utils.database import session, Base, engine
from sqlalchemy import  Column, String
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


# Office class
class Office(Base):
    __tablename__ = "offices"

    officeCode = Column(String(10), primary_key=True)
    city = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    addressLine1 = Column(String(50), nullable=False)
    addressLine2 = Column(String(50))
    state = Column(String(50))
    country = Column(String(50), nullable=False)
    postalCode = Column(String(15), nullable=False)
    territory = Column(String(10), nullable=False)

    def __init__(self, officeCode, city, phone, addressLine1, addressLine2, state, country, postalCode, territory):
        self.officeCode = officeCode
        self.city = city
        self.phone = phone
        self.addressLine1 = addressLine1
        self.addressLine2 = addressLine2
        self.state = state
        self.country = country
        self.postalCode = postalCode
        self.territory = territory


# Office schema
class OfficeSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Office
        sqla_session = session

    officeCode = fields.String(required=True)       # dump_only=True --> only reading, to Autocompleted primary key, autocreated Date, file path
    city = fields.String(required=True)
    phone = fields.String(required=True)
    addressLine1 = fields.String(required=True)
    addressLine2 = fields.String()
    state = fields.String()                         # In POST is required to evade error
    country = fields.String(required=True)
    postalCode = fields.String(required=True)
    territory = fields.String(required=True)