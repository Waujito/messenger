import logging
from uuid import UUID
from .chatsSerivce import get_chat_or_error
from ..db.models import ChatInvite, ChatMembership, User
from ..db import db
from sqlalchemy import select
from werkzeug.exceptions import Forbidden, NotFound, BadRequest
from ..auth.usersService import get_user_or_error as get_member_or_error


def get_chat_members(user: User, chat_id: int):
    """Lists chat members"""
    chat = get_chat_or_error(chat_id)
    membership = get_user_chat_membership(chat_id, user.id)

    if not membership:
        raise Forbidden()

    return chat.members  # todo: Implement paging


def get_user_chat_membership(chat_id: int, user_id: int) -> ChatMembership | None:
    """Returns user's membership with the chat by chat_id and user_id or None if the user is not a member"""
    return db.session.scalars(
        select(ChatMembership).where(ChatMembership.chat_id ==
                                     chat_id).where(ChatMembership.user_id == user_id)
    ).first()


def ensure_membership(chat_id: int, user_id: int):
    """Checks the user to be a member of the chat. Returns chat and membership or throws Forbidden"""

    chat = get_chat_or_error(chat_id)
    membership = get_user_chat_membership(chat_id, user_id)

    if not membership:
        raise Forbidden()

    return chat, membership


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


def add_member(chat_id: int, member_id: int):
    # Check the user to be not in the chat already
    membership = get_user_chat_membership(chat_id, member_id)

    if membership is not None:
        raise BadRequest('The user is already in the chat.')

    membership = ChatMembership()

    chatMembership = ChatMembership(chat_id=chat_id, user_id=member_id)
    db.session.add(chatMembership)
    db.session.commit()

    return chatMembership


def generate_invite(user: User, chat_id: int) -> ChatInvite:
    """
    Generates an invite link to the chat
    """

    chat = get_chat_or_error(chat_id)
    if chat.owner != user:
        raise Forbidden()

    invite = ChatInvite(chat_id=chat_id)

    db.session.add(invite)
    db.session.commit()

    return invite


def process_invite_code(invite_code: str) -> ChatInvite:
    try:
        uuid_code = UUID(invite_code)
    except ValueError:
        raise BadRequest('Invalid invite code.')

    invite = db.session.scalars(select(ChatInvite).where(
        ChatInvite.code == uuid_code)).first()

    if not invite:
        raise NotFound('An invite code is not exist.')

    return invite


def join_by_invite_code(user: User, invite_code: str) -> ChatMembership:
    invite = process_invite_code(invite_code)

    membership = add_member(invite.chat_id, user.id)

    return membership


def get_all_invites(user: User, chat_id: int) -> list[ChatInvite]:
    chat = get_chat_or_error(chat_id)

    if chat.owner != user:
        raise Forbidden()

    return chat.invites


def delete_invite(user: User, chat_id: int, invite_id: int):
    invite = db.session.scalars(select(ChatInvite).where(
        ChatInvite.id == invite_id)).first()

    if not invite:
        raise NotFound("An invite is not found.")

    chat = invite.chat

    if chat_id != chat.id:
        raise BadRequest()

    if user != chat.owner:
        raise Forbidden()

    db.session.delete(invite)
    db.session.commit()
