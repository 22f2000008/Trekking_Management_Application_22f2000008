from datetime import timedelta


class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///trekkingDb.sqlite3'
    JWT_SECRET_KEY = "this-is-a-secret-key"

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)