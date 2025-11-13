from datetime import datetime, timezone
from typing import Optional
import uuid
from enum import Enum

from pydantic import BaseModel, ConfigDict, field_serializer
from sqlalchemy import Column, DateTime, String, Text, ForeignKey, Integer

from app.db.schema import Base
from app.core.utils.helpers import to_camel_case


class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column[str](
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    user_id = Column[str](String(36), ForeignKey("users.id"), nullable=True, index=True)

    title = Column[str](String(255), nullable=False)
    description = Column[str](Text, nullable=True)
    location = Column[str](String(255), nullable=True)
    date = Column[datetime](DateTime(timezone=False), nullable=False)
    time = Column[str](
        String(50), nullable=True
    )  # Store time as string (e.g., "14:30")
    duration = Column[int](Integer, nullable=True)
    status = Column[str](String(50), nullable=True)  # AppointmentStatus enum
    with_person = Column[str](String(255), nullable=True)
    notes = Column[str](Text, nullable=True)
    preparation_time = Column[int](Integer, nullable=True)
    created_at = Column[datetime](
        DateTime(timezone=False), nullable=True, default=datetime.now(timezone.utc)
    )
    updated_at = Column[datetime](
        DateTime(timezone=False),
        nullable=True,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:  # pragma: no cover - tiny helper
        return f"<Appointment id={self.id} title={self.title!r}>"


class AppointmentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    date: datetime
    time: Optional[str] = None
    duration: Optional[int] = None
    status: Optional[str] = None  # AppointmentStatus
    with_person: Optional[str] = None
    notes: Optional[str] = None
    preparation_time: Optional[int] = None

    model_config = ConfigDict(alias_generator=to_camel_case, populate_by_name=True)


class AppointmentRead(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    date: datetime  # Will be serialized to ISO string
    time: Optional[str] = None
    duration: Optional[int] = None
    status: Optional[str] = None
    with_person: Optional[str] = None
    notes: Optional[str] = None
    preparation_time: Optional[int] = None
    created_at: Optional[datetime] = None  # Will be serialized to ISO string
    updated_at: Optional[datetime] = None  # Will be serialized to ISO string
    user_id: Optional[str] = None

    @field_serializer("date", "created_at", "updated_at", when_used="json")
    def serialize_datetime(self, value: Optional[datetime], _info) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.isoformat()
        return str(value)

    model_config = ConfigDict(
        from_attributes=True, alias_generator=to_camel_case, populate_by_name=True
    )
