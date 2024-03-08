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

    # From this index response array will be started,
    # direction of starting (down or up) is determined according to `loadDirection` argument
    startingIndex = int(request.args["startIdx"]
                        ) if "startIdx" in request.args else -1

    # Limits amount of message to load per each request. Internal maximum is 5000, default is 1000
    messagesLimit = min(
        int(request.args["limit"]), 5000) if "limit" in request.args else 1000

    # Specifies the direction to pagination. -1 = goes down, from startingIndex to the last message
    # 1 = from startingIndex to the earlies message, up to messagesLimit
    loadDirection = - \
        1 if "loadDirection" in request.args and request.args["loadDirection"] == "-1" else 1

    query = select(Message).where(Message.chat_id == chat_id)

    if startingIndex != -1:
        if loadDirection == 1:
            query = query.where(Message.id <= startingIndex)
            query = query.order_by(Message.created_at.desc())
        else:
            query = query.where(Message.id >= startingIndex)
            query = query.order_by(Message.created_at.asc())
    else:
        query = query.order_by(Message.created_at.desc())

    query = query.limit(messagesLimit)

    messages = db.session.scalars(query).all()

    if startingIndex != -1 and loadDirection != 1:
        messages = messages.__reversed__()

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
