"""
To define the basic config that we did in main.py and
then adds environment-specific configuration on the top.
"""

class Config(object):
    DEBUG = True
    PORT = 5000
    HOST = "127.0.0.1"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://<db_user>:<db_pass>@<db_host>:<port>/<db_name>"
    # TESTING = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://<db_user>:<db_pass>@<db_host>:<port>/<db_name>"
    SQLALCHEMY_ECHO = False
    # UPLOAD_FOLDER= '<upload_folder>'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://<db_user>:<db_pass>@<db_host>:<port>/<db_name>"
    SQLALCHEMY_ECHO = False
    # UPLOAD_FOLDER= '<upload_folder>'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://<db_user>:<db_pass>@<db_host>:<port>/<db_name>"
    SQLALCHEMY_ECHO = False
    # UPLOAD_FOLDER= '<upload_folder>'