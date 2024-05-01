from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..serializers.messages import MessageCreate, MessageDisplay, MessagesDisplay
from typing import List
from ..repositories.messages_repository import MessagesRepository

router = APIRouter()
messages_repository = MessagesRepository()


@router.post("/{chat_id}", response_model=MessageDisplay)
async def send_message(
    chat_id: int, message_data: MessageCreate, db: Session = Depends(get_db)
):
    return messages_repository.send_message(db, chat_id, message_data)


@router.get("/{chat_id}", response_model=List[MessagesDisplay])
async def connect_to_chat(chat_id: int, user_id: int, db: Session = Depends(get_db)):
    messages = messages_repository.get_messages(db, chat_id, user_id)
    return [
        MessagesDisplay(
            id=msg.id,
            content=msg.content,
            created_at=msg.created_at,
            sender_email=msg.sender.email,
        )
        for msg in messages
    ]
