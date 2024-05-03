from fastapi import APIRouter, Depends, Response, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from ..database.database import get_db
from sqlalchemy.orm import Session
from pydantic import EmailStr
from ..serializers.users import UserCreate, UserInfo, UserLogin, UserUpdate
from ..serializers.chats import ChatBase
from ..repositories.users_repository import UsersRepository
from typing import List

router = APIRouter()
users_repository = UsersRepository()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt(user_id: int) -> str:
    body = {"user_id": user_id}
    token = jwt.encode(body, "shanyrak_secret", "HS256")
    return token


def decode_jwt(token: str) -> int:
    data = jwt.decode(token, "shanyrak_secret", "HS256")
    return data["user_id"]


# registration
@router.post("/register")
def post_signup(
    user_input: UserCreate,
    db: Session = Depends(get_db),
):
    user_input.password = hash_password(user_input.password)
    new_user = users_repository.create_user(db, user_input)
    return Response(
        status_code=200, content=f"successfull signup. User_id = {new_user.id}"
    )


# login
@router.post("/login")
def post_login(
    # user_input: UserLogin,
    username: EmailStr = Form(),
    password: str = Form(),
    db: Session = Depends(get_db),
):
    user_data = UserLogin(email=username, password=password)
    user = users_repository.get_user_by_email(db, user_data)
    if not verify_password(password, user.password_hashed):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_jwt(user.id)
    print(access_token)
    return {"access_token": access_token, "token_type": "bearer"}


# update user
@router.patch("/me")
def patch_user(
    user_input: UserUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    user_id = decode_jwt(token)
    user_input.password = hash_password(user_input.password)
    users_repository.update_user(db, user_id, user_input)
    return Response(content="User updated successfully", status_code=200)


# get user info
@router.get("/me", response_model=UserInfo)
def get_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_jwt(token)
    user = users_repository.get_by_id(db, user_id)
    user.phone = user.phone.replace("-", " ")
    return UserInfo(
        id=user_id,
        email=user.email,
        phone=user.phone[4:],
        username=user.username,
        city=user.city,
    )


@router.get("/chats", response_model=List[ChatBase])
async def get_all_chats(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    user_id = decode_jwt(token)
    user_chats = users_repository.get_user_chats(db, user_id)
    return user_chats
