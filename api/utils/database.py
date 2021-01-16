#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Create database connection and instances
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Create engine declarative, configure mysql connection
engine = create_engine('mysql+pymysql://root:@localhost/test', echo=True)  # , encoding='latin1')

# Create base declarative
Base = declarative_base()

# Create session declarative
Session = sessionmaker(bind=engine)

# Base.metadata.create_all(engine)        # "???"