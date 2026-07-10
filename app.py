from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from flask_mail import Mail
from celery import Celery
from werkzeug.security import generate_password_hash

from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import User
from application.security import jwt

app = None

cache = Cache()
celery = Celery(__name__)
mail = Mail()


def create_app():

    app = Flask(__name__)

    app.config.from_object(LocalDevelopmentConfig)
     
    # Extensions
    
    db.init_app(app)

    jwt.init_app(app)

    cache.init_app(app)

    mail.init_app(app)

    # Celery Configuration

    celery.conf.broker_url = app.config["BROKER_URL"]

    celery.conf.result_backend = app.config["RESULT_BACKEND"]

    CORS(app)

    return app


app = create_app()

from application.routes import *


if __name__ == "__main__":

    with app.app_context():

        db.create_all()

        admin = User.query.filter_by(
            role="admin"
        ).first()

        if not admin:

            admin = User(

                username="admin",

                email="admin@gmail.com",

                password=generate_password_hash("1234"),

                role="admin"

            )

            db.session.add(admin)

            db.session.commit()

        print("Admin Created Successfully")

    app.run(debug=True)