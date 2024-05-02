from pydantic import BaseModel, validator
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
    sender: str
    content: str
    created_at: datetime

    @validator('created_at', pre=True, allow_reuse=True)
    def format_datetime(cls, value: datetime):
        # Ensure the value is a datetime object and then format it
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        return value