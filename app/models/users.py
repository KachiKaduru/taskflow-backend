from typing import Optional
import uuid

from pydantic import BaseModel
from sqlalchemy import Column, String

from app.db.schema import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
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
    id: uuid.UUID
    name: str
    email: str
    image: Optional[str] = None
