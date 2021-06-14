#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Create database connection and instances
"""

from sqlalchemy import create_engine
from api.config.config import app_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Create engine declarative, configure mysql connection
engine = create_engine(app_config.SQLALCHEMY_DATABASE_URI)
# echo=True, use_unicode=True o  convert_unicode = True, encoding="utf8" o encoding='latin1'

# Create 'Session' declarative.
# Session class is defined using 'sessionmaker()'function which is bound to the engine object. To interact with the database, we need its handle, which is a 'session' object. 'bind' - The database Engine to which to bind the session
Session = sessionmaker(bind=engine)
session = Session()

# Create 'Base' declarative.
# The 'declarative_base()' function is used to create 'base' class. A base class stores a catlog of classes and mapped tables in the Declarative system.
Base = declarative_base()