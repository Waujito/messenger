from . import db, Model
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Text, Index
from datetime import datetime
from typing import List
from .mixins import TimestampMixin


class User(TimestampMixin, Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)

    password: Mapped[str] = mapped_column(String(255))

    chats: Mapped[List["Chat"]] = relationship(
        secondary="chat_memberships", back_populates="members")
    messages: Mapped[List["Message"]] = relationship(back_populates="author")

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, User):
            return self.id == __value.id
        else:
            return super().__eq__(__value)


class ChatMembership(TimestampMixin, Model):
    __tablename__ = "chat_memberships"
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"))
    chat_id: Mapped[int] = mapped_column(
        ForeignKey("chats.id", ondelete="CASCADE"))

    user: Mapped[User] = relationship(lazy="joined")
    chat: Mapped["Chat"] = relationship(lazy="joined")

    def to_json(self):
        return {
            "id": self.id,
            "user": self.user.to_json(),
            "chat": self.chat.to_json(),
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __eq__(self, __value: type["ChatMembership"]) -> bool:
        return self.id == __value.id


class Chat(TimestampMixin, Model):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(255))

    owner_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id", ondelete="SET NULL"), nullable=True)
    owner: Mapped[User] = relationship()

    messages: Mapped[List["Message"]] = relationship(back_populates="chat")
    members: Mapped[List[User]] = relationship(
        secondary=ChatMembership.__tablename__, back_populates="chats")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "owner_id": self.owner_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __eq__(self, __value: type["Chat"]) -> bool:
        return self.id == __value.id


class Message(TimestampMixin, Model):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)

    content: Mapped[int] = mapped_column(Text)

    chat_id: Mapped[int] = mapped_column(
        ForeignKey("chats.id", ondelete="CASCADE"))
    chat: Mapped[Chat] = relationship(back_populates="messages", lazy="joined")

    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    author: Mapped[User] = relationship(
        back_populates="messages", lazy="joined")

    def to_json(self):
        return {
            "id": self.id,
            "content": self.content,
            "author": self.author.to_json(),
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __eq__(self, __value: type["Message"]) -> bool:
        return self.id == __value.id


class ChatInvite(TimestampMixin, Model):
    __tablename__ = "chatInvites"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(255))

    chat_id: Mapped[int] = mapped_column(
        ForeignKey("chats.id", ondelete="CASCADE")
    )
    chat: Mapped[Chat] = relationship(lazy="joined")

    def to_json(self):
        return {
            "id": self.id,
            "code": self.code,
            "chat_id": self.chat_id,
            "created_at": self.created_at
        }
