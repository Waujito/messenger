from ..messagingAPI.chatsSerivce import get_chat_or_error, get_user_chat_membership
from ..db.models import User
from werkzeug.exceptions import Forbidden


def get_chat_members(user: User, chat_id: int):
    """Lists chat members"""
    chat = get_chat_or_error(chat_id)
    membership = get_user_chat_membership(chat_id, user.id)

    if not membership:
        raise Forbidden()

    return chat.members  # todo: Implement paging
