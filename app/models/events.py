from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.db.schema import Base


class Event(Base):
    """SQLAlchemy ORM table for events.

    Fields map to the frontend `newEvent` shape sent in the prompt.
    """

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    start_time = Column(DateTime(timezone=False), nullable=False)
    end_time = Column(DateTime(timezone=False), nullable=False)
    is_virtual = Column(Boolean, default=False, nullable=False)
    event_type = Column(String(100), nullable=True)

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


class EventRead(EventCreate):
    id: int

    # Use pydantic v2 config to allow reading from ORM objects
    model_config = ConfigDict(from_attributes=True)
