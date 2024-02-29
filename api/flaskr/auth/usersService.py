from ..db.models import db, User
from sqlalchemy import select
from werkzeug.exceptions import NotFound

def get_user(user_id) -> User | None:
    """Returns the user or none if it is not present"""
    return db.session.get(User, user_id)


def get_user_or_error(user_id) -> User:
    """Returns the user or throws an exception if is is not present"""

    user = get_user(user_id)
    if not user:
        raise NotFound("The user is not found.")
    
    return user

