from ..messagingAPI.chatsSerivce import get_chat_or_error, get_user_chat_membership
from ..db.models import ChatMembership, User
from ..db import db
from werkzeug.exceptions import Forbidden, NotFound
from ..auth.usersService import get_user_or_error as get_member_or_error


def get_chat_members(user: User, chat_id: int):
    """Lists chat members"""
    chat = get_chat_or_error(chat_id)
    membership = get_user_chat_membership(chat_id, user.id)

    if not membership:
        raise Forbidden()

    return chat.members  # todo: Implement paging


def get_membership(user: User, chat_id: int, member_id: int | None = None) -> ChatMembership:
    """
    Returns the membership with chat by `chat_id` and member by  `member_id`.
    If `member_id` is null returns the membership of current user.
    """

    member = get_member_or_error(member_id) if member_id is not None else user

    membership = get_user_chat_membership(chat_id, member.id)
    user_membership = get_user_chat_membership(chat_id, user.id)

    if not user_membership:
        raise Forbidden()

    if membership:
        return membership
    else:
        raise NotFound("The user is not a member of the chat")


def kick_member(user: User, chat_id: int, member_id: int | None = None):
    """
    Kicks the user `member_id` (deletes the membership) of chat `chat_id`.
    """

    chat = get_chat_or_error(chat_id)

    member = get_member_or_error(member_id) if member_id is not None else user

    membership = get_user_chat_membership(chat_id, member.id)

    if not user == chat.owner:
        raise Forbidden()

    if membership:
        db.session.delete(membership)
        db.session.commit()
    else:
        raise NotFound("The user is not a member of the chat")
