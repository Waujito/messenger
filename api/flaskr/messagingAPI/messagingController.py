from . import api
from flask import request, jsonify, Response
from ..db.models import User, db, Chat, ChatMembership, Message
from sqlalchemy import select
from werkzeug.exceptions import BadRequest, NotFound, Forbidden, MethodNotAllowed

from jsonschema import validate
from .jsonschema import chatCreationRequestSchema
from .chatsSerivce import get_chat_or_error, get_user_chat_membership, ensure_membership
from ..auth.usersService import get_user as get_member, get_user_or_error as get_member_or_error
from .messagesService import get_message_or_error
import re

blankRegex = re.compile(r'^\s*$')


def get_user() -> User:
    return request.user  # type: ignore


@api.route("/chats/<int:chat_id>/messages", methods=["POST"])
def send_message(chat_id: int):
    user = get_user()

    chat, membership = ensure_membership(chat_id, user.id)

    message_content = request.data.decode()

    if blankRegex.match(message_content):
        raise BadRequest("Message cannot be empty.")

    message = Message(content=message_content,
                      chat_id=chat_id, author_id=user.id)

    db.session.add(message)
    db.session.commit()

    return jsonify(message.to_json()), 201


@api.route("/chats/<int:chat_id>/messages", methods=["GET"])
def get_chat_messages(chat_id: int):
    user = get_user()

    chat, membership = ensure_membership(chat_id, user.id)

    # messages = chat.messages
    messages = db.session.scalars(select(Message).where(
        Message.chat_id == chat_id).order_by(Message.created_at.desc()))

    # todo: add paging
    return jsonify(list(map(lambda x: x.to_json(), messages)))


@api.route("/chats/<int:chat_id>/messages/<int:message_id>", methods=["PUT", "DELETE"])
def manageMessage(chat_id, message_id):
    user = get_user()

    chat, membership = ensure_membership(chat_id, user.id)

    message = get_message_or_error(message_id, chat_id)

    # Delete the message
    if request.method == "DELETE":
        # Only author and chat owner may delete messages
        if not (message.author == user or user == chat.owner):
            raise Forbidden()

        db.session.delete(message)
        db.session.commit()

        return Response(status=204)
    elif request.method == "PUT":
        # Only author may update the message
        if not (message.author == user):
            raise Forbidden()

        message_content = request.data.decode()

        if blankRegex.match(message_content):
            raise BadRequest("Message cannot be empty.")

        message.content = message_content  # type: ignore

        db.session.commit()

        return jsonify(message.to_json())
    else:
        raise MethodNotAllowed()
