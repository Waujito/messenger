from . import api
from flask import request, jsonify, Response
from ..db.models import User, db, Chat, ChatMembership
from sqlalchemy import select
from werkzeug.exceptions import BadRequest, NotFound, Forbidden, MethodNotAllowed

from jsonschema import validate
from .jsonschema import chatCreationRequestSchema
from .chatsSerivce import get_chat_or_error, get_user_chat_membership
from ..auth.usersService import get_user as get_member, get_user_or_error as get_member_or_error


def get_user() -> User:
    return request.user  # type: ignore



@api.route("/chats/<int:chat_id>/members", methods=["GET"])
def get_chat_members(chat_id):
    user = get_user()

    chat = get_chat_or_error(chat_id)
    membership = get_user_chat_membership(chat_id, user.id)

    if not membership:
        raise Forbidden()
    
    return chat.members #todo: Implement paging
    

@api.route("/chats/<int:chat_id>/members/<int:member_id>", methods=["GET", "POST", "DELETE"])
def chats_member_methods(chat_id, member_id):
    user = get_user()

    chat = get_chat_or_error(chat_id)
    chat_owner = chat.owner
    
    member = get_member_or_error(member_id)
    
    membership = get_user_chat_membership(chat_id, member_id)
    user_membership = get_user_chat_membership(chat_id, user.id)

    # Handle GET method. Return the membership
    if request.method == "GET":
        if not user_membership:
            raise Forbidden()
        
        if membership:
            return jsonify(membership.to_json())
        else:
            raise NotFound("The user is not a member of the chat")
    # Add the user to the chat
    elif request.method == "POST":
        if user != chat_owner:
            raise Forbidden()

        if membership:
            raise BadRequest("The user is already member of the chat.")
        
        membership = ChatMembership(
            chat_id = chat.id,
            user_id = member.id
        )

        db.session.add(membership)
        db.session.commit()

        return Response(status=201)
    # Kick the user
    elif request.method == "DELETE":
        # member may be deleted from chat by chat owner or leave by itself
        if user != chat_owner and not (user.id == member_id and membership is not None):
            raise Forbidden()
        
        if not membership:
            return NotFound("The user is not a member of the chat")
        
        db.session.delete(membership)
        db.session.commit()

        return Response(status=204)
    else: 
        # to suppress pylance error
        raise MethodNotAllowed()

