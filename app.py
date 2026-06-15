from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import Admin, Trek_Staff, User
from application.security import jwt

app = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    jwt.init_app(app)
    app.app_context().push()
    return app

app = create_app()

#from application.routes import *

if __name__ == '__main__':
    #db.create_all()
    #db.session.add(User(username="batman", email="batman@example.com", password="1234"))
    #db.session.add(User(username="panther", email="panther@example.com", password="1234"))
    #db.session.commit()

    app.run()