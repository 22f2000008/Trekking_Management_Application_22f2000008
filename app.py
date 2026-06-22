from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import User
from application.security import jwt

from werkzeug.security import generate_password_hash

app = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    jwt.init_app(app)
    app.app_context().push()
    return app

app = create_app()

from application.routes import *

if __name__ == '__main__':
    db.create_all()
    
    admin = User.query.filter_by(role='admin').first()

    if not admin:
        admin = User(username="admin", email="admin@gmail.com", password=generate_password_hash("1234"), role="admin")

    db.session.add(admin)
    db.session.commit()
    print("Admin Created Successfully")

    app.run(debug=True)