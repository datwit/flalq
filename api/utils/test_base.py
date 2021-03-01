#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module acts as a temporary replacement for a called module, providing the same output as the actual product.
Run before every test is run and it spawns a new test client. Import this methods in all the tests created.
"""


import unittest2 as unittest
from main import create_app
from api.config.config import app_config
from sqlalchemy import create_engine
from api.utils.database import session, Base


class BaseTestCase(unittest.TestCase):
    """A base test case"""

    def setUp(self):
        """This method is called once, before every test method; to create the mysql database and all tables. """

        self.app = create_app(app_config)
        # print(self.app.config)
        self.client = self.app.test_client
        self.engine = create_engine(app_config.SQLALCHEMY_DATABASE_URI)
        with self.app.app_context():
            Base.metadata.create_all(self.engine)
        self.app.app_context().push()



    def tearDown(self):
        """This method is called once, after every test method; to close current session and to delete test-database completely """

        with self.app.app_context():
            session.close()
            Base.metadata.drop_all(self.engine)
        # self.app_context.pop()