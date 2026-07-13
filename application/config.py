from datetime import timedelta

class Config:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
    # Redis Cache
   
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_DEFAULT_TIMEOUT = 60

     
    # Celery Configuration
    
    BROKER_URL = "redis://localhost:6379/0"
    RESULT_BACKEND = "redis://localhost:6379/0"

     
    # Flask-Mail Configuration
     
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

     
    MAIL_USERNAME = "22f2000008@ds.study.iitm.ac.in"

    MAIL_PASSWORD = "tvkt gdli bhts mpbs"

    MAIL_DEFAULT_SENDER = "22f2000008@ds.study.iitm.ac.in"


class LocalDevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///trekkingDb.sqlite3"

    JWT_SECRET_KEY = "this-is-a-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)