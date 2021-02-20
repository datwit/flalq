#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Create database connection and instances
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Create engine declarative, configure mysql connection
engine = create_engine('mysql+pymysql://root:@localhost/pruebadanay', echo=True)
# use_unicode=True o  convert_unicode = True, charset="utf8" o encoding='latin1'

# # To create 'Session' declarative.
# # Session class is defined using 'sessionmaker()'function which is bound to the engine object. To interact with the database, we need its handle, which is a 'session' object. 'bind' - The database Engine to which to bind the session
Session = sessionmaker(bind=engine)

# To create 'Base' declarative.
# The 'declarative_base()' function is used to create 'base' class. A base class stores a catlog of classes and mapped tables in the Declarative system.
Base = declarative_base()