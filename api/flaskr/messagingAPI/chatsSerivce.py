from ..db.models import db, Chat, ChatMembership
from sqlalchemy import select
from werkzeug.exceptions import NotFound, Forbidden


def get_chat(chat_id: int) -> Chat | None:
    """Returns the Chat by chat_id or None if the chat is not exist"""
    return db.session.get(Chat, chat_id)

def get_chat_or_error(chat_id: int) -> Chat:
    """Returns the Chat by chat_id or throws a NotFound exception if the chat is not exist"""
    chat = get_chat(chat_id)
    if not chat:
        raise NotFound("Chat is not found.")
    
    return chat

def get_user_chat_membership(chat_id: int, user_id: int) -> ChatMembership | None:
    """Returns user's membership with the chat by chat_id and user_id or None if the user is not a member"""
    return db.session.scalars(
        select(ChatMembership).where(ChatMembership.chat_id == chat_id and ChatMembership.user_id == user_id)
    ).first()

def ensure_membership(chat_id: int, user_id: int):
    """Checks the user to be a member of the chat. Returns chat and membership or throws Forbidden"""

    chat = get_chat_or_error(chat_id)
    membership = get_user_chat_membership(chat_id, user_id)

    if not membership: raise Forbidden()

    return chat, membership

