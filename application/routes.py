from flask import current_app as app, jsonify, request, abort
from .models import User
from flask_jwt_extended import create_access_token, current_user, jwt_required

@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"wrong email or password"}), 401
    

    #Notice that we are passing in the actual sqlalchemy user obejct
    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)