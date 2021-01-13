#!/usr/bin/python
# -*- coding: utf-8 -*-

from main import app
from api.config import config

# # If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)