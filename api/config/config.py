""""
To define the basic configuration that we did in main.py and
then adds environment-specific configuration on top.
"""

import os

class Config(object):
    """Configure 'Config' base class with environment general variables"""

    DEBUG = True
    # PORT = 5000
    # HOST = "127.0.0.1"
    SQLALCHEMY_ECHO = False
    # To Disable that a sign must be sended every time that an object is modified
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://<db_user>:<db_pass>@<db_host>:<port>/<db_name>"
    # UPLOAD_FOLDER= '<upload_folder>'
    # ALLOWED_EXTENSIONS = '<upload_file_extensions>'
    # MAX_CONTENT_LENGTH = '<upload_top_file_size>'
    TESTING = False
    # SERVER_NAME = '127.0.0.1:5000'
    # PAGINATION_PAGE_SIZE = 5
    # PAGINATION_PAGE_ARGUMENT_NAME = 'page'
    # # Disable CSRF protection in the testing configuration
    # WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Configure 'ProductionConfig' class with 'Production' environment specific variables"""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@127.0.0.1:3306/pruebadanay"
    SQLALCHEMY_ECHO = False
    UPLOAD_FOLDER= 'C:/Users/Danay/Desktop/danay_python/snippets/api_classic/api/images/'
    ALLOWED_EXTENSIONS = {'png', 'jpg'}
    MAX_CONTENT_LENGTH = 0.1 * 1024 * 1024
    APP_ENV_PRODUCTION = 'production'


class DevelopmentConfig(Config):
    """Configure 'DevelopmentConfig' class with 'Development' environment specific variables"""

    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@127.0.0.1:3306/pruebadanay"
    SQLALCHEMY_ECHO = False
    UPLOAD_FOLDER= 'C:/Users/Danay/Desktop/danay_python/snippets/api_classic/api/images/'
    ALLOWED_EXTENSIONS = {'png', 'jpg'}
    MAX_CONTENT_LENGTH = 0.1 * 1024 * 1024
    APP_ENV_DEVELOPMENT = 'development'


class TestingConfig(Config):
    """Configure 'TestingConfig' class with 'Testing' environment specific variables"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@127.0.0.1:3306/testing"
    SQLALCHEMY_ECHO = False
    UPLOAD_FOLDER= 'C:/Users/Danay/Desktop/danay_python/snippets/api_classic/api/images/'
    ALLOWED_EXTENSIONS = {'png', 'jpg'}
    MAX_CONTENT_LENGTH = 0.1 * 1024 * 1024
    APP_ENV_TESTING = 'testing'


""" To configure variables by environment."""

if os.environ.get('FLASK_ENV') == 'production':
    app_config = ProductionConfig
elif os.environ.get('FLASK_ENV') == 'testing':
    app_config = TestingConfig
else:
    app_config = DevelopmentConfig