from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..database.models import Chat, Message
from ..serializers.messages import MessageCreate


class MessagesRepository:
    def send_message(
        self, db: Session, chat_id: int, message_data: MessageCreate
    ) -> Message:
        chat = (
            db.query(Chat)
            .filter(Chat.id == chat_id, Chat.users.any(id=message_data.user_id))
            .first()
        )
        if not chat:
            raise HTTPException(
                status_code=404, detail="Chat not found or user not part of chat"
            )

        new_message = Message(
            content=message_data.content,
            sender_id=message_data.user_id,
            chat_id=chat_id,
        )
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        return new_message

    def get_messages(self, db: Session, chat_id: int, user_id: int):
        chat = (
            db.query(Chat)
            .filter(Chat.id == chat_id, Chat.users.any(id=user_id))
            .first()
        )
        if not chat:
            raise HTTPException(
                status_code=404, detail="Chat not found or access denied"
            )

        messages = db.query(Message).filter(Message.chat_id == chat_id).all()
        return messages
