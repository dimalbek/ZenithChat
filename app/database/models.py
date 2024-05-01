from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    DateTime,
)
from sqlalchemy.orm import relationship
from .database import Base
import pytz
from datetime import datetime

# Association table for the many-to-many relationship between users and chats
chat_user_table = Table(
    "chat_user",
    Base.metadata,
    Column("chat_id", Integer, ForeignKey("chats.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    password_hashed = Column(String, nullable=False)
    username = Column(String, nullable=False)
    city = Column(String, nullable=False)

    chats = relationship("Chat", secondary=chat_user_table, back_populates="users")
    messages = relationship("Message", back_populates="sender")


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)
    users = relationship("User", secondary=chat_user_table, back_populates="chats")
    messages = relationship("Message", back_populates="chat")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(pytz.timezone("Asia/Almaty")))
    sender_id = Column(Integer, ForeignKey("users.id"))
    chat_id = Column(Integer, ForeignKey("chats.id"))

    sender = relationship("User", back_populates="messages")
    chat = relationship("Chat", back_populates="messages")
