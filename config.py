import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_DEBUG = False
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300


class DevelopmentConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True


class ProductionConfig(Config):
    FLASK_ENV = "production"


class TestingConfig(Config):
    FLASK_ENV = "testing"


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
