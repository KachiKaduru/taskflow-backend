from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Boolean, Column, DateTime, String, Text, ForeignKey

from app.db.schema import Base
from app.core.utils.helpers import to_camel_case


class Event(Base):
    __tablename__ = "events"

    event_id = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    start_time = Column(DateTime(timezone=False), nullable=False)
    end_time = Column(DateTime(timezone=False), nullable=False)
    is_virtual = Column(Boolean, default=False, nullable=False)
    event_type = Column(String(100), nullable=True)

    def __repr__(self) -> str:  # pragma: no cover - tiny helper
        return f"<Event id={self.event_id} title={self.title!r}>"


# Pydantic models (v2) for request/response shapes
class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: datetime
    end_time: datetime
    is_virtual: bool = False
    event_type: Optional[str] = None

    model_config = ConfigDict(alias_generator=to_camel_case, populate_by_name=True)


class EventRead(EventCreate):
    id: uuid.UUID
    model_config = ConfigDict(
        from_attributes=True, alias_generator=to_camel_case, populate_by_name=True
    )
