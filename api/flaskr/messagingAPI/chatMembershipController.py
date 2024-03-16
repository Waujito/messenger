from . import api
from flask import request, jsonify, Response
from ..db.models import User

from .chatMembershipService import delete_invite, generate_invite, get_all_invites, get_chat_members as get_chat_members_service, get_membership, join_by_invite_code, kick_member, process_invite_code


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


@api.route('/chats/<int:chat_id>/invites', methods=["POST"])
def create_invite(chat_id: int):
    user = get_user()

    invite = generate_invite(user, chat_id)

    return jsonify(invite.to_json()), 201


@api.route('/chats/<int:chat_id>/invites', methods=["GET"])
def get_invites(chat_id: int):
    user = get_user()

    invites = get_all_invites(user, chat_id)

    return jsonify(list(map(lambda x: x.to_json(), invites)))


@api.route('/chats/<int:chat_id>/invites/<int:invite_id>', methods=["DELETE"])
def delete_chat_invite(chat_id: int, invite_id: int):
    user = get_user()

    delete_invite(user, chat_id, invite_id)

    return Response(status=204)


@api.route('/chats/invites/<invite_code>', methods=["GET"])
def check_invite(invite_code: str):
    invite = process_invite_code(invite_code)

    return jsonify(invite.to_json())


@api.route('/chats/invites/<invite_code>/join', methods=["POST"])
def join_chat_by_invite_code(invite_code: str):
    user = get_user()

    membership = join_by_invite_code(user, invite_code)

    return jsonify(membership.to_json()), 201
