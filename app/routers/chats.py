from fastapi import APIRouter, Depends, Response, Form
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..serializers.chats import ChatBase
from typing import List, Optional
from ..repositories.chats_repository import ChatsRepository
from .users import decode_jwt


router = APIRouter()
chats_repository = ChatsRepository()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


@router.get("/all", response_model=List[ChatBase])
async def get_all_chats(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    user_id = decode_jwt(token)
    all_chats = chats_repository.get_all_chats(db, user_id)
    return all_chats


@router.post("/new/", response_model=ChatBase)
async def create_chat(
    password: Optional[str] = Form(None),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_jwt(token)
    new_chat = chats_repository.create_chat(db, user_id, password)
    return Response(
        status_code=200, content=f"chat with id {new_chat.id} created"
    )


@router.post("/join/{chat_id}", response_model=ChatBase)
async def add_user_to_chat(
    chat_id: int,
    password: Optional[str] = Form(None),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_jwt(token)
    joined_chat = chats_repository.add_user_to_chat(
        db, chat_id, user_id, password
    )
    return Response(
        status_code=200,
        content=f"user with id {user_id} joined to chat with id {joined_chat.id}"
    )
