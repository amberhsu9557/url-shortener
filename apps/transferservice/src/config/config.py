import os
import datetime
from datetime import timedelta
from dotenv import load_dotenv
from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(override=True)


class BaseConfig:

    # Logs Collection
    LOG_DIR = '/tmp/logs'

    # Session
    SECRET_KEY = os.getenv('SECRET_KEY')
    PERMANENT_SESSION_LIFETIME = timedelta(days=14)

    # Transfer
    MAX_URL_LEN = int(os.getenv("MAX_URL_LEN", default="2000"))
    DB_EXPIRED_TIME = int(os.getenv("DB_EXPIRED_TIME", default="31536000"))

    # Postgres
    DB = {
        'user': os.getenv('POSTGRES_USER', default='postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', default='micro'),
        'db': 'transferservice',
        'host': 'transferdb',
        'port': '5432',
    }

    # Flask-sqlalchemy
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(password)s@%(host)s:%(port)s/%(db)s' % DB
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 3600,
        "pool_timeout": 900,
        "pool_size": 10,
        "max_overflow": 5,
    }

    # Redis
    REDIS_USERNAME = 'default'
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', default='redis')

    # Cache
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL= f'redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@redis:6379/0'

    # Celery
    # CELERY_* settings in config and have Celery use those values
    # https://docs.celeryproject.org/en/stable/userguide/configuration.html
    CELERY_TIMEZONE = 'Asia/Taipei'
    BROKER_URL = f'redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@redis:6379/1'
    CELERY_RESULT_BACKEND = f'redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@redis:6379/2'


class DevelopConfig(BaseConfig):
    # development mode
    DEBUG = bool(os.getenv("FLASK_DEBUG", default=True))

    # Flask-sqlalchemy (development, testing)
    SQLALCHEMY_ECHO = True if DEBUG else False
    # SQLALCHEMY_DATABASE_URI = 'postgresql://amber:amber@db:5432/stc'
    # SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/test.db"

    # # Disabled CSRF (development, testing)
    WTF_CSRF_ENABLED = False if DEBUG else True

    # # Celery (development, testing)
    # CELERY_BROKER_URL = f'redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@redis:6379/2"
    # CELERY_RESULT_BACKEND =  f'redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@redis:6379/2"
    # # CELERY_RDB_HOST default is localhost
    # # to allow RDB able to be connected outside the container CELERY_RDB_HOST
    # # is needed to be something else rather than localhost
    # CELERY_RDB_HOST='redis'
    # # # Default debugging port 6900 or customized by yourself
    # CELERY_RDB_PORT = 6900


class ProductionConfig(BaseConfig):
    DEBUG = bool(os.getenv("FLASK_DEBUG", default=False))


class TestConfig(BaseConfig):
    TESTING = True

    # Flask-sqlalchemy (development, testing)
    # SQLALCHEMY_ECHO = True if TESTING else False
    # SQLALCHEMY_DATABASE_URI = 'postgresql://amber:amber@db:5432/stc'
    # SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/test.db"

    # # Disabled CSRF (development, testing)
    # WTF_CSRF_ENABLED = False if TESTING else True

    # # Celery (development, testing)
    # CELERY_BROKER_URL = f'redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@redis:6379/1"
    # CELERY_RESULT_BACKEND =  f'redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@redis:6379/2"
    # # CELERY_RDB_HOST default is localhost
    # # to allow RDB able to be connected outside the container CELERY_RDB_HOST
    # # is needed to be something else rather than localhost
    # CELERY_RDB_HOST='0.0.0.0'
    # # # Default debugging port 6900 or customized by yourself
    # CELERY_RDB_PORT = 6900


config = {
    "production": ProductionConfig,
    "develop": DevelopConfig,
    "test": TestConfig,
    "default": DevelopConfig,
}
