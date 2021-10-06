import re
from app import db, jwt
from app.auth import bp
from app.auth.helpers import getUsers, getUser, addUser, removeUser
from app.models import Users, InvalidToken
from app.security import encpwd, checkpwd, enc, dec
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt, \
    jwt_required


@jwt.token_in_blocklist_loader
def check_if_blacklisted_token(data, decrypted):
    """
    Decorator designed to check for blacklisted tokens
    """
    jti = decrypted['jti']
    return InvalidToken.is_invalid(jti)


@bp.route("/api/login", methods=["POST"])
def login():
    """
    User login end-point accepts email and password.
    returns jwt_token
    """
    try:
        email = request.json["email"]
        pwd = request.json["pwd"]
        if email and pwd:
            user = list(filter(lambda x: dec(x["email"]) == email and checkpwd(pwd, x["pwd"]), getUsers()))
            if len(user) == 1:
                token = create_access_token(identity=user[0]["id"])
                refresh_token = create_refresh_token(identity=user[0]["id"])
                return jsonify({"token": token, "refreshToken": refresh_token})
            else:
                return jsonify({"error": "Invalid credentials"})
        else:           
            return jsonify({"error":"Invalid Form"})
    except:
        return jsonify({"error": "Invalid Form"})


@bp.route("/api/register", methods=["POST"])
def register():
    """
    End-point to handle user registration, encrypting the password and validating the email
    """
    try:
        pwd = encpwd(request.json['pwd'])
        username = request.json['username']
        email = request.json["email"]
        email = email.lower()
        
        users = getUsers()
        if len(list(filter(lambda x: dec(x["email"]) == email, users))) == 1:         
            return jsonify({"error": "Invalid Form"})

        if not re.match(r"[\w\._]{5,}@\w{3,}.\w{2,4}", email):
            return jsonify({"error": "Invalid form"})
        # secure details validate username
        addUser(username, enc(email), pwd)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)})


@bp.route("/api/checkiftokenexpire", methods=["POST"])
@jwt_required()
def check_if_token_expire():
    """
    End-point for frontend to check if the token has expired or not
    """
    return jsonify({"success": True})


@bp.route("/api/refreshtoken", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
    End-point to refresh the token when required
    
    """
    identity = get_jwt_identity()
    token = create_access_token(identity=identity)
    return jsonify({"token": token})


@bp.route("/api/logout/access", methods=["POST"])
@jwt_required()
def access_logout():
    """
    End-point to log the user out and Invalidate the token.
    """
    jti = get_jwt()["jti"]
    try:
        invalid_token = InvalidToken(jti=jti)
        invalid_token.save()
        return jsonify({"success":True})
    except Exception as e:
        print(e)
        return jsonify({"error": e})


@bp.route("/api/logout/refresh", methods=["POST"])
@jwt_required()
def refresh_logout():
    
    jti = get_jwt()["jti"]
    try:
        invalid_token = InvalidToken(jti=jti)
        invalid_token.save()
        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return jsonify({"error": e})


@bp.route("/api/getcurrentuser")
@jwt_required()
def current_user():
    """
    End-point to handle collecting the current user information
    """
    uid = get_jwt_identity()
    return jsonify(getUser(uid))


@bp.route("/api/deleteaccount", methods=["DELETE"])
@jwt_required()
def delete_account():
    """
    End-point to handle removal of users
    """
    try:
        user = Users.query.get(get_jwt_identity())
        removeUser(user.id)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)})