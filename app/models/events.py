from datetime import datetime, timezone
from typing import Optional
import uuid

from pydantic import BaseModel, ConfigDict, field_serializer
from sqlalchemy import Boolean, Column, DateTime, String, Text, ForeignKey

from app.db.schema import Base
from app.core.utils.helpers import to_camel_case


class Event(Base):
    __tablename__ = "events"

    id = Column[str](
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    user_id = Column[str](String(36), ForeignKey("users.id"), nullable=True, index=True)

    title = Column[str](String(255), nullable=False)
    description = Column[str](Text, nullable=True)
    location = Column[str](String(255), nullable=True)
    start_time = Column[datetime](DateTime(timezone=False), nullable=False)
    end_time = Column[datetime](DateTime(timezone=False), nullable=False)
    is_virtual = Column[bool](Boolean, default=False, nullable=False)
    event_type = Column[str](String(100), nullable=True)
    status = Column[str](
        String(50), nullable=True
    )  # e.g., "scheduled", "cancelled", "completed"
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
        return f"<Event id={self.id} title={self.title!r}>"


# Pydantic models (v2) for request/response shapes
class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: datetime
    end_time: datetime
    is_virtual: bool = False
    event_type: Optional[str] = None
    status: Optional[str] = None

    model_config = ConfigDict(alias_generator=to_camel_case, populate_by_name=True)


class EventRead(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: datetime
    end_time: datetime
    is_virtual: bool = False
    event_type: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    user_id: Optional[str] = None

    @field_serializer(
        "start_time", "end_time", "created_at", "updated_at", when_used="json"
    )
    def serialize_datetime(self, value: Optional[datetime], _info) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.isoformat()
        return str(value)

    model_config = ConfigDict(
        from_attributes=True, alias_generator=to_camel_case, populate_by_name=True
    )
