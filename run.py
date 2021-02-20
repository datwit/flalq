#!/usr/bin/python
# -*- coding: utf-8 -*-

""" To call app and run the application """

from main import app as application


# If we're running in stand alone mode, run the application
if __name__ == "__main__":
    application.run()