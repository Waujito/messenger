from os import name

from flaskr.messagingAPI.sockets.chatSockets import MessagingNamespace
from ..db.models import User, db, Chat, Message
from sqlalchemy import select
from werkzeug.exceptions import NotFound, Forbidden, BadRequest
from .chatsSerivce import ensure_membership, get_chat_or_error
import re
from .sockets import socketio

blankRegex = re.compile(r'^\s*$')


def get_message_or_error(message_id: int, chat: int | Chat) -> Message:
    """Returns the message from the chat"""
    if not isinstance(chat, Chat):
        chat = get_chat_or_error(chat)

    message = db.session.get(Message, message_id)

    if not message or message.chat != chat:
        raise NotFound("The message is not found")

    return message


def post_message(user: User, chat_id: int, messageContent: str):
    """
    Posts the message sent by user.
    Returns message.
    """
    chat, membership = ensure_membership(chat_id, user.id)

    if blankRegex.match(messageContent):
        raise BadRequest("Message cannot be empty.")

    message = Message(content=messageContent,
                      chat_id=chat_id, author_id=user.id)

    db.session.add(message)
    db.session.commit()

    socketio.emit("messageSent", {"chat_id": chat.id, "message": message.to_json()}, namespace="/chat",
                  to=MessagingNamespace.chat_to_room(chat))

    return message


def list_messages(user: User, chat_id: int, limit=1000, startingIndex: int = -1, loadDirection=1):
    """
    Lists all messages sent in chat. Supports pagination.
    Params:
    `user` - user,\n
    `chat_id` - chat id,\n
    `limit` - Limits amount of message to load per each request. Internal maximum is 5000, default is 1000\n
    `startingIndex` - From this index response array will be started, direction of starting 
    (down or up) is determined according to `loadDirection` argument\n
    `loadDirection` - Specifies the direction to pagination. -1 = goes down, 
    from startingIndex to the last message 1 = from startingIndex to the earliest message, up to messagesLimit \n
    """
    chat, membership = ensure_membership(chat_id, user.id)

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

    query = query.limit(limit)

    messages = db.session.scalars(query).all()

    if startingIndex != -1 and loadDirection != 1:
        messages = messages.__reversed__()

    return messages


def deleteMessage(user: User, chat_id: int, message_id: int):
    """Deletes message."""
    chat, membership = ensure_membership(chat_id, user.id)

    message = get_message_or_error(message_id, chat_id)

    # Only author and chat owner may delete messages
    if not (message.author == user or user == chat.owner):
        raise Forbidden()

    db.session.delete(message)
    db.session.commit()


def updateMessage(user: User, chat_id: int, message_id: int, messageContent: str):
    """Updates the message"""
    chat, membership = ensure_membership(chat_id, user.id)
    message = get_message_or_error(message_id, chat_id)

    # Only author may update the message
    if not (message.author == user):
        raise Forbidden()

    if blankRegex.match(messageContent):
        raise BadRequest("Message cannot be empty.")

    message.content = messageContent  # type: ignore

    db.session.commit()

    return message
