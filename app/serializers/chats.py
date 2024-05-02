from pydantic import BaseModel
from typing import List


class ChatBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ChatDisplay(BaseModel):
    id: int
    name: str
    is_private: bool

    class Config:
        orm_mode = True


class PaginatedChatResponse(BaseModel):
    total: int
    chats: List[ChatDisplay]
