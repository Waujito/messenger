from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from . import jsonschema
from jsonschema.exceptions import ValidationError
from jsonschema import validate
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden
from flask import request, jsonify, current_app
from sqlalchemy import select
import jwt
from functools import wraps

import datetime as dt

from inspect import getfullargspec

from . import auth, www_authenticate

from ..db import models, db
User = models.User

ph = PasswordHasher()


@auth.route("/register", methods=["POST"])
def register():
    data = request.json

    validate(data, jsonschema.userRegisterSchema)
    if not isinstance(data, dict):
        raise ValueError()

    username: str = data["username"]
    password: str = data["password"]
    password_hash = ph.hash(password)

    if db.session.scalars(select(User.username).where(User.username == username)).first() is not None:
        raise BadRequest("Username is already taken")

    user = User(
        username=username,
        password=password_hash
    )

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_json())


@auth.route("/login", methods=["POST"])
def login():
    data = request.json

    validate(data, jsonschema.userLoginSchema)
    if not isinstance(data, dict):
        raise ValueError()

    username: str = data["username"]
    password: str = data["password"]

    user = db.session.scalars(select(User).where(
        User.username == username)).first()

    try:
        if user is None:
            raise VerifyMismatchError()

        ph.verify(user.password, password)
    except VerifyMismatchError:
        raise BadRequest("Username or password is incorrect")

    issuer = current_app.config["JWT_ISSUER"]
    issued_at = dt.datetime.utcnow()
    expiration_time = issued_at + dt.timedelta(days=7)

    jwt_body = {
        "sub": user.id,
        "iss": issuer,
        "iat": issued_at,
        "exp": expiration_time
    }

    secret_key = current_app.config["SECRET_KEY"]

    encoded_jwt = jwt.encode(jwt_body, secret_key, algorithm="HS256")

    return encoded_jwt


def authorize_user(scope: str | None = None):
    # OPTIONS requests should be open
    if request.method == 'OPTIONS':
        return None, None

    authorization = request.authorization

    if authorization is None:
        raise Unauthorized(www_authenticate=www_authenticate)

    token = authorization.token
    if authorization.type != "bearer" or token is None:
        raise Unauthorized(www_authenticate=www_authenticate)

    secret_key = current_app.config["SECRET_KEY"]
    issuer = current_app.config["JWT_ISSUER"]

    try:
        decoded_jwt = jwt.decode(
            token, secret_key, issuer=issuer, algorithms=["HS256"])
    except:
        raise Unauthorized(www_authenticate=www_authenticate)

    sub = decoded_jwt["sub"]

    user = db.session().get(User, sub)

    if not user:
        raise Unauthorized("User is not found.",
                           www_authenticate=www_authenticate)

    if scope is not None:  # todo: Implement scopes
        raise Forbidden()

    return user, token


def authorized(scope: str | None = None):
    """
    Ensures user authorization, processes authorization scopes.
    Authenticates the user via JWT.
    Provides user object and jwt token with `user` and `token` kwargs to the route method
    """
    def decorator(f):
        @wraps(f)
        def auth_func(*args, **kwargs):
            user, token = authorize_user()

            funcArgs = getfullargspec(f)
            if "user" in funcArgs.args or funcArgs.varkw is not None:
                kwargs["user"] = user
            if "token" in funcArgs.args or funcArgs.varkw is not None:
                kwargs["token"] = token

            return f(*args, **kwargs)

        return auth_func
    return decorator


@auth.route("/user")
@authorized()
def user(user: User):
    return jsonify(user.to_json())
