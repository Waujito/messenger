from . import api
from flask import request, jsonify, Response
from ..db.models import User, db, Chat, ChatMembership
from sqlalchemy import select
from werkzeug.exceptions import BadRequest, NotFound

from jsonschema import validate
from .jsonschema import chatCreationRequestSchema

from .chatsSerivce import get_chat, get_chat_or_error


def get_user() -> User:
    return request.user  # type: ignore


@api.route("/chats", methods=["POST"])
def create_chat():
    user = get_user()

    data = request.json
    validate(data, chatCreationRequestSchema)
    if not isinstance(data, dict):
        raise BadRequest()

    chat = Chat(name=data["name"], owner_id=user.id)
    db.session.add(chat)
    db.session.flush()

    chatMembership = ChatMembership(chat_id=chat.id, user_id=user.id)
    db.session.add(chatMembership)
    db.session.commit()

    return jsonify(chat.to_json()), 201


@api.route("/chats", methods=["GET"])
def get_chats():
    user = get_user()

    chats = user.chats

    return jsonify(list(map(lambda x: x.to_json(), chats)))

@api.route("/chats/<int:chat_id>", methods=["DELETE"])
def delete_chat(chat_id: int):
    chat = get_chat_or_error(chat_id)

    db.session.delete(chat)
    db.session.commit()

    return Response(status=204)