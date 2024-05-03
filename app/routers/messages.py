from fastapi import APIRouter, Depends, Response, WebSocket, HTTPException
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
from ..websocket_manager import manager
from starlette.websockets import WebSocketDisconnect
from starlette import status
from starlette.responses import StreamingResponse
import json
from ..database.models import Message
import asyncio


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
            sender=msg.sender.username,
            content=msg.content,
            created_at=msg.created_at,
        )
        for msg in messages
    ]


@router.get("/stream/{chat_id}", response_class=StreamingResponse)
async def stream_chat_messages(chat_id: int, db: Session = Depends(get_db)):
    async def event_stream():
        last_id = 0
        while True:
            # fetch for new messages
            messages = db.query(Message).filter(Message.chat_id == chat_id, Message.id > last_id).order_by(Message.id.asc()).all()
            if messages:
                last_id = messages[-1].id
                for message in messages:
                    yield f"data: {json.dumps(MessagesDisplay.from_orm(message).dict())}\n\n"
            await asyncio.sleep(1)  # sleep for second

    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'text/event-stream',
        'Connection': 'keep-alive',
    }
    return StreamingResponse(event_stream(), headers=headers)


@router.websocket("/ws/{chat_id}")
async def websocket_chat(
    websocket: WebSocket,
    chat_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        # user_id = 1
        user_id = decode_jwt(token)
        if not messages_repository.is_user_in_chat(db, user_id, chat_id):
            await websocket.close(code=1000)
            return

        await manager.connect(websocket, chat_id)
        try:
            while True:
                message_data = await websocket.receive_text()
                await manager.broadcast(chat_id, message_data)
        except WebSocketDisconnect:
            manager.disconnect(websocket, chat_id)
    except HTTPException as e:
        await websocket.close(code=status.HTTP_401_UNAUTHORIZED)
        print(f"Failed to authenticate: {str(e)}")
    except Exception as e:
        await websocket.close(code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print(f"Error: {str(e)}")
