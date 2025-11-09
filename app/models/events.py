from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, ForeignKey

from app.db.schema import Base
from app.core.utils.helpers import to_camel_case


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
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

    model_config = ConfigDict(alias_generator=to_camel_case, populate_by_name=True)


class EventRead(EventCreate):
    id: int

    # Allow building from ORM attributes and output aliases in camelCase
    model_config = ConfigDict(
        from_attributes=True, alias_generator=to_camel_case, populate_by_name=True
    )
