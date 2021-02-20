#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module acts as a temporary replacement for a called module providing the same output as the actual product.
Run before every test is run and it spawns a new test client. Import this method in all the tests created.
"""


import unittest2 as unittest
from main import app
from sqlalchemy import create_engine
from api.config.config import TestingConfig
from api.utils.database import Base, Session

session = Session()

# def create_app(config_filename):
#     """
#     Create app
#     """
#     # app initialization
#     app = Flask(__name__)
#     # initialize app from object depending on environment
#     app.config.from_object(config_filename)
#     return app

class BaseTestCase(unittest.TestCase):
    """A base test case"""

    def setUp(self):
        """This method is called once, before every test method; to create the mysql database and all tables. """

        app.config.from_object(TestingConfig)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/testing'
        # push context in order to get app instance in other modules
        with app.app_context():
            engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
            Base.metadata.create_all(bind=engine)
        app.app_context().push()
        self.client = app.test_client()


    def tearDown(self):
        """This method is called once, after every test method; to close current session and to delete test-database completely """

        with app.app_context():
            engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
            session.close()
            Base.metadata.drop_all(engine)
        # self.app_context.pop()