from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..serializers.messages import (
    MessageCreate,
    MessageDisplay,
    MessagesDisplay
)
from typing import List
from ..repositories.messages_repository import MessagesRepository
from .users import decode_jwt


router = APIRouter()
messages_repository = MessagesRepository()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


@router.post("/{chat_id}", response_model=MessageDisplay)
async def send_message(
    chat_id: int,
    message_data: MessageCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    user_id = decode_jwt(token)
    new_message = messages_repository.send_message(db, chat_id, user_id, message_data)
    return Response(
        status_code=200,
        content=f"message with id {new_message.id} sent to chat with id {new_message.chat_id}"
    )


@router.get("/{chat_id}", response_model=List[MessagesDisplay])
async def connect_to_chat(
    chat_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_jwt(token)
    messages = messages_repository.get_messages(db, chat_id, user_id)
    return [
        MessagesDisplay(
            sender_email=msg.sender.email,
            content=msg.content,
            created_at=msg.created_at,
        )
        for msg in messages
    ]
