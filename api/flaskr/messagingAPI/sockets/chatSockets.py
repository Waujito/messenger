import logging
from shlex import join
from flask import jsonify, session
from flask_socketio import emit, join_room
from flask_socketio.namespace import Namespace
from socketio import server

from flaskr.db.models import Chat, User


from flaskr.auth.userController import authorize_jwt, authorize_socketio
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden, HTTPException

from flaskr.messagingAPI.chatMembershipService import ensure_membership


class MessagingNamespace(Namespace):
    def on_connect(self, data: dict | None):
        authorize_socketio(data)

    def on_user(self):
        logging.critical("usersdjf;sdlkfj")
        return session['user'].to_json()

    def on_subscribe(self, data: dict | None):
        """
        Subscribes the user to the chat messages.
        """

        if type(data) is not dict or "chat_id" not in data:
            raise BadRequest()

        chat_id = data["chat_id"]
        user: User = session["user"]

        chat, membership = ensure_membership(chat_id, user.id)

        room = self.chat_to_room(chat)

        join_room(room)

        return 0

    @staticmethod
    def chat_to_room(chat: Chat) -> str:
        return str(chat.id)
