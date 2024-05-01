from pydantic import BaseModel

class ChatBase(BaseModel):
    id: int

    class Config:
        orm_mode = True
