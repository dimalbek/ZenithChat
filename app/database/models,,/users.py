from sqlalchemy import (
    Column,
    Integer,
    String,
)
from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    password_hashed = Column(String, nullable=False)
    username = Column(String, nullable=False)
    city = Column(String, nullable=False)
