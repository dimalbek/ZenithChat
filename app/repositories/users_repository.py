from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ..database.models.users import User
from ..serializers.users import UserCreate, UserLogin, UserUpdate


class UsersRepository:
    def create_user(self, db: Session, user_data: UserCreate) -> User:
        try:
            # Check if the user already exists
            existing_user = db.query(User).filter(
                    User.email == user_data.email).first()

            if existing_user:
                raise HTTPException(
                    status_code=400, detail="User already exists")

            new_user = User(
                email=user_data.email,
                phone=user_data.phone,
                password_hashed=user_data.password,
                username=user_data.username,
                city=user_data.city,
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)

        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=400,
                                detail=f"Integrity error: {str(e)}")
        return new_user

    def get_user_by_email(self, db: Session, user_data: UserLogin) -> User:
        db_user = db.query(User).filter(
            User.email == user_data.email).first()
        if not db_user:
            print(f"User with email {user_data.email} not found")
            raise HTTPException(status_code=404, detail="User not found")
        return db_user

    def update_user(self, db: Session, user_id: int, user_data: UserUpdate):
        db_user = db.query(User).filter(User.id == user_id).first()

        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        for field, value in user_data.model_dump(exclude_unset=True).items():
            setattr(db_user, field, value)

        try:
            db.commit()
            db.refresh(db_user)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Invalid user data")

    def get_by_id(self, db: Session, user_id: int) -> User:
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
