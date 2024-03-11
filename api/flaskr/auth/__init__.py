from flask import Blueprint
from werkzeug.datastructures import WWWAuthenticate

www_authenticate = WWWAuthenticate("Bearer")

auth = Blueprint("auth", __name__)

from . import userController  # noqa
