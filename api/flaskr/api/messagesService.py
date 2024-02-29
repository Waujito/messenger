from ..db.models import db, Chat, ChatMembership, Message
from sqlalchemy import select
from werkzeug.exceptions import NotFound, Forbidden
from .chatsSerivce import get_chat_or_error

def get_message_or_error(message_id: int, chat: int|Chat) -> Message:
    """Returns the message from the chat"""
    if not isinstance(chat, Chat):
        chat = get_chat_or_error(chat)

    message = db.session.get(Message, message_id)

    if not message or message.chat != chat:
        raise NotFound("The message is not found")

    return message
