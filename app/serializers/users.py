from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserCreate(BaseModel):
    email: EmailStr
    phone: PhoneNumber = "+7 --- --- ----"
    password: str
    username: str
    city: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: EmailStr = None
    phone: PhoneNumber = None
    password: str = None
    username: str = None
    city: str = None


class UserInfo(BaseModel):
    id: int
    email: EmailStr
    phone: str
    username: str
    city: str
