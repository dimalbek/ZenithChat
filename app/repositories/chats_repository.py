from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..database.models import User, Chat
from passlib.context import CryptContext
from typing import Optional
from sqlalchemy import func


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ChatsRepository:
    def create_chat(
        self,
        db: Session,
        user_id: int,
        name: str,
        password: Optional[str] = None
    ) -> Chat:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        new_chat = Chat(
            name=name,
            is_private=bool(password),
            password_hashed=pwd_context.hash(password) if password else None,
            users=[user]
        )
        db.add(new_chat)
        db.commit()
        return new_chat

    def add_user_to_chat(
        self,
        db: Session,
        chat_id: int,
        user_id: int,
        password: Optional[str] = None
    ) -> Chat:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        chat = db.query(Chat).filter(Chat.id == chat_id).first()
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        if user in chat.users:
            raise HTTPException(status_code=400, detail="User already in chat")

        if chat.is_private:
            if not password:
                raise HTTPException(
                    status_code=403, detail="Missing password for private chat"
                )
            if not pwd_context.verify(password, chat.password_hashed):
                raise HTTPException(
                    status_code=403,
                    detail="Incorrect password for private chat"
                )

        user = db.query(User).get(user_id)
        chat.users.append(user)
        db.commit()
        return chat

    def get_all_chats(self, db: Session, skip: int = 0, limit: int = 10):
        chats = db.query(Chat.id, Chat.name, Chat.is_private
                         ).offset(skip).limit(limit).all()
        total = db.query(func.count(Chat.id)).scalar()
        return chats, total
