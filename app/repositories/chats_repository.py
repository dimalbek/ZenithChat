from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..database.models import User, Chat


class ChatsRepository:
    def get_all_chats(self, db: Session, user_id: int) -> list:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user.chats

    def create_chat(self, db: Session, user_id: int) -> Chat:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        new_chat = Chat(users=[user])
        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)
        return new_chat

    def add_user_to_chat(self, db: Session, chat_id: int, user_id: int) -> Chat:
        user = db.query(User).filter(User.id == user_id).first()
        chat = db.query(Chat).filter(Chat.id == chat_id).first()
        if not user or not chat:
            raise HTTPException(status_code=404, detail="User or Chat not found")
        if user in chat.users:
            raise HTTPException(status_code=400, detail="User already in chat")
        chat.users.append(user)
        db.commit()
        db.refresh(chat)
        return chat
