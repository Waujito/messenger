from . import api
from flask import request, jsonify, Response
from ..db.models import User

from .chatMembershipService import get_chat_members as get_chat_members_service, get_membership, kick_member


def get_user() -> User:
    return request.user  # type: ignore


@api.route("/chats/<int:chat_id>/members", methods=["GET"])
def get_chat_members(chat_id):
    user = get_user()

    members = get_chat_members_service(user, chat_id)

    return jsonify(list(map(lambda x: x.to_json(), members)))


@api.route("/chats/<int:chat_id>/members/<int:member_id>", methods=["GET"])
def get_member(chat_id, member_id):
    user = get_user()

    membership = get_membership(user, chat_id, member_id)

    return jsonify(membership.to_json())


@api.route("/chats/<int:chat_id>/members/@me", methods=["GET"])
def get_self_membership(chat_id, member_id):
    user = get_user()

    membership = get_membership(user, chat_id)

    return jsonify(membership.to_json())


@api.route("/chats/<int:chat_id>/members/<int:member_id>", methods=["DELETE"])
def delete_memberhip(chat_id, member_id):
    user = get_user()

    kick_member(user, chat_id, member_id)

    return Response(status=204)
