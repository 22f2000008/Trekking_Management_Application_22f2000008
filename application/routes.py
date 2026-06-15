from flask import current_app as app, jsonify, request, abort
from .models import User, Admin, Trek_Staff
from flask_jwt_extended import create_access_token, current_user, jwt_required

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(username=username).one_or_none()
    if not user or not user.password == password:
        return jsonify({"wrong username or password"}), 401
    

    #Notice that we are passing in the actual sqlalchemy user obejct
    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)