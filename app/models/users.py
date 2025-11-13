from typing import Optional
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer
from sqlalchemy import Column, String, DateTime

from app.db.schema import Base
from app.core.utils.helpers import to_camel_case


class Users(Base):
    __tablename__ = "users"

    id = Column[str](
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    name = Column[str](String(255), nullable=False)
    email = Column[str](String(255), unique=True, index=True, nullable=False)
    image = Column[str](String, nullable=True)
    hashed_password = Column[str](String, nullable=False)
    created_at = Column[datetime](
        DateTime(timezone=False), nullable=True, default=datetime.utcnow
    )
    updated_at = Column[datetime](
        DateTime(timezone=False),
        nullable=True,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class UsersCreate(BaseModel):
    name: str
    email: str
    image: Optional[str] = None
    password: str

    model_config = ConfigDict(alias_generator=to_camel_case, populate_by_name=True)


class UsersRead(BaseModel):
    id: str
    name: str
    email: str
    image: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_serializer("created_at", "updated_at", when_used="json")
    def serialize_datetime(self, value: Optional[datetime], _info) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.isoformat()
        return str(value)

    model_config = ConfigDict(
        from_attributes=True, alias_generator=to_camel_case, populate_by_name=True
    )
