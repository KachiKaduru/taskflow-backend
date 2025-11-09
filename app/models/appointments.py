from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db.schema import Base
from app.core.utils.helpers import to_camel_case


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    with_person = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    date = Column(DateTime(timezone=False), nullable=False)
    duration = Column(Integer, nullable=True)
    preparation_time = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)

    def __repr__(self) -> str:  # pragma: no cover - tiny helper
        return f"<Appointment id={self.id} title={self.title!r}>"


class AppointmentCreate(BaseModel):
    title: str
    with_person: Optional[str] = None
    location: Optional[str] = None
    date: datetime
    duration: Optional[int] = None
    preparation_time: Optional[int] = None
    notes: Optional[str] = None

    model_config = ConfigDict(alias_generator=to_camel_case, populate_by_name=True)


class AppointmentRead(AppointmentCreate):
    id: int
    model_config = ConfigDict(
        from_attributes=True, alias_generator=to_camel_case, populate_by_name=True
    )
