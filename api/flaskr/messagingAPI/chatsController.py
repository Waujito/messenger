from . import api
from flask import request, jsonify, Response
from ..db.models import User, db, Chat, ChatMembership
from sqlalchemy import select
from werkzeug.exceptions import BadRequest, NotFound

from jsonschema import validate
from .jsonschema import chatCreationRequestSchema

from .chatsSerivce import get_chat, get_chat_or_error, create_chat as create_chat_service, get_user_chats, delete_chat as delete_chat_service


def get_user() -> User:
    return request.user  # type: ignore


@api.route("/chats", methods=["POST"])
def create_chat():
    user = get_user()

    data = request.json
    if not isinstance(data, dict):
        raise BadRequest()

    chat, membership = create_chat_service(user, data)

    return jsonify(chat.to_json()), 201


@api.route("/chats", methods=["GET"])
def get_chats():
    user = get_user()

    chats = get_user_chats(user)

    return jsonify(list(map(lambda x: x.to_json(), chats)))


@api.route("/chats/<int:chat_id>", methods=["DELETE"])
def delete_chat(chat_id: int):
    user = get_user()

    delete_chat_service(user, chat_id)

    return Response(status=204)
