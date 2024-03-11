from http.client import BAD_REQUEST
from jsonschema import validate
from ..db.models import User, db, Chat, ChatMembership
from sqlalchemy import select
from werkzeug.exceptions import NotFound, Forbidden, BadRequest
from .jsonschema import chatCreationRequestSchema
import re

blankRegex = re.compile(r'^\s*$')


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
        select(ChatMembership).where(ChatMembership.chat_id ==
                                     chat_id and ChatMembership.user_id == user_id)  # type: ignore
    ).first()


def ensure_membership(chat_id: int, user_id: int):
    """Checks the user to be a member of the chat. Returns chat and membership or throws Forbidden"""

    chat = get_chat_or_error(chat_id)
    membership = get_user_chat_membership(chat_id, user_id)

    if not membership:
        raise Forbidden()

    return chat, membership


def create_chat(user: User, data: dict) -> tuple[Chat, ChatMembership]:
    """
    Creates the chat, adds the user to the chat.
    user: user object, data: json object, must follow the type defined in jsonschema
    Returns tuple of Chat, ChatMembership objects 
    """

    validate(data, chatCreationRequestSchema)
    if blankRegex.match(data["name"]):
        raise BadRequest("Chat name cannot be empty")

    chat = Chat(name=data["name"], owner_id=user.id)
    db.session.add(chat)
    db.session.flush()

    chatMembership = ChatMembership(chat_id=chat.id, user_id=user.id)
    db.session.add(chatMembership)
    db.session.commit()

    return chat, chatMembership


def get_user_chats(user: User) -> list[Chat]:
    """
    Returns all user's chats
    """
    return user.chats


def delete_chat(user: User, chat_id: int):
    """
    Deletes the chat
    """

    chat = get_chat_or_error(chat_id)
    if chat.owner_id != user.id:
        raise Forbidden()

    db.session.delete(chat)
    db.session.commit()
