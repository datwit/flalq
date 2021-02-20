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
    UPLOAD_FOLDER= '<upload_folder>'
    ALLOWED_EXTENSIONS = '<upload_file_extensions>'
    MAX_CONTENT_LENGTH = '<upload_top_file_size>'
    TESTING = False
    # SERVER_NAME = '127.0.0.1:5000'
    # PAGINATION_PAGE_SIZE = 5
    # PAGINATION_PAGE_ARGUMENT_NAME = 'page'
    # # Disable CSRF protection in the testing configuration
    # WTF_CSRF_ENABLED = False
    # SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost:5000/pruebadanay"
    SQLALCHEMY_ECHO = False
    UPLOAD_FOLDER= 'C:/Users/Danay/Desktop/danay_python/snippets/api_classic/api/images/'
    ALLOWED_EXTENSIONS = {'png', 'jpg'}
    MAX_CONTENT_LENGTH = 0.1 * 1024 * 1024
    APP_ENV_PRODUCTION = 'production'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost:5000/pruebadanay"
    SQLALCHEMY_ECHO = False
    UPLOAD_FOLDER= 'C:/Users/Danay/Desktop/danay_python/snippets/api_classic/api/images/'
    ALLOWED_EXTENSIONS = {'png', 'jpg'}
    MAX_CONTENT_LENGTH = 0.1 * 1024 * 1024
    APP_ENV_DEVELOPMENT = 'development'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@127.0.0.1:3306/testing"
    SQLALCHEMY_ECHO = False
    UPLOAD_FOLDER= 'C:/Users/Danay/Desktop/danay_python/snippets/api_classic/api/images/'
    ALLOWED_EXTENSIONS = {'png', 'jpg'}
    MAX_CONTENT_LENGTH = 0.1 * 1024 * 1024
    APP_ENV_TESTING = 'testing'