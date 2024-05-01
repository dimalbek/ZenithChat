from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..serializers.chats import ChatBase
from typing import List
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
    return chats_repository.get_all_chats(db, user_id)


@router.post("/new/", response_model=ChatBase)
async def create_chat(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_jwt(token)
    return chats_repository.create_chat(db, user_id)


@router.post("/new/{chat_id}", response_model=ChatBase)
async def add_user_to_chat(
    chat_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_jwt(token)
    return chats_repository.add_user_to_chat(db, chat_id, user_id)
