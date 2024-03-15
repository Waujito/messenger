from ..auth.userController import authorize_http
from flask import Blueprint, request

api = Blueprint("api", __name__)


def authorize_mdl():
    user, token = authorize_http()

    request.user = user  # type: ignore
    request.token = token  # type: ignore


api.before_request(authorize_mdl)

from . import chatMembershipController, chatsController, messagingController  # noqa
