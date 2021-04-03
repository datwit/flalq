#!/usr/bin/python
# -*- coding: utf-8 -*-

""" To call app and run the application """

from api.config.config import app_config
from main import create_app


application = create_app(app_config)


# If we're running in stand alone mode, run the application
if __name__ == "__main__":
    application.run(host= app_config.HOST, port=app_config.PORT, debug=app_config.DEBUG)
    # because when I not use 'debug=True' in run, even if app_config has 'DEBUG=TRUE', the application run on 'Debug mode: off'