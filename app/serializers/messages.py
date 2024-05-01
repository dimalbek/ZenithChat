from pydantic import BaseModel
from datetime import datetime


class MessageCreate(BaseModel):
    content: str


class MessageDisplay(BaseModel):
    id: int
    content: str
    created_at: datetime
    sender_id: int
    chat_id: int

    class Config:
        orm_mode = True


class MessageBase(BaseModel):
    id: int
    content: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True


class MessagesDisplay(BaseModel):
    sender_email: str
    content: str
    created_at: datetime
