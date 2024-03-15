from . import api
from flask import request, jsonify, Response
from ..db.models import User
from .messagesService import list_messages, post_message, updateMessage, deleteMessage as deleteMessageService


def get_user() -> User:
    return request.user  # type: ignore


@api.route("/chats/<int:chat_id>/messages", methods=["POST"])
def send_message(chat_id: int):
    user = get_user()

    message_content = request.data.decode()
    message = post_message(user, chat_id, message_content)

    return jsonify(message.to_json()), 201


@api.route("/chats/<int:chat_id>/messages", methods=["GET"])
def get_chat_messages(chat_id: int):
    user = get_user()

    startingIndex = int(request.args["startIdx"]
                        ) if "startIdx" in request.args else -1

    messagesLimit = min(
        int(request.args["limit"]), 5000) if "limit" in request.args else 1000

    loadDirection = - \
        1 if "loadDirection" in request.args and request.args["loadDirection"] == "-1" else 1

    messages = list_messages(user, chat_id, limit=messagesLimit,
                             startingIndex=startingIndex, loadDirection=loadDirection)

    return jsonify(list(map(lambda x: x.to_json(), messages)))


@api.route("/chats/<int:chat_id>/messages/<int:message_id>", methods=["PUT"])
def editMessage(chat_id, message_id):
    user = get_user()

    message_content = request.data.decode()

    message = updateMessage(user, chat_id, message_id, message_content)

    return jsonify(message.to_json())


@api.route("/chats/<int:chat_id>/messages/<int:message_id>", methods=["DELETE"])
def deleteMessage(chat_id, message_id):
    user = get_user()

    deleteMessageService(user, chat_id, message_id)

    return Response(status=204)
