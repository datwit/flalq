#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""

from flask import Flask

app = Flask(__name__)


# If we're running in stand alone mode, run the application
if __name__ == "__main__":
    app.run(host='localhost', port=4000, debug=True)   # (..., use_reloader=False)???