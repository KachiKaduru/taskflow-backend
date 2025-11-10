from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, String, Integer

from app.db.schema import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    image = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)


class UsersCreate(BaseModel):
    name: str
    email: str
    image: Optional[str] = None
    password: str


class UsersRead(BaseModel):
    id: int
    name: str
    email: str
    image: Optional[str] = None
