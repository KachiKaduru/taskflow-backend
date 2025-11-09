from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db.schema import Base


def _to_camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(p.title() for p in parts[1:])


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

    model_config = ConfigDict(alias_generator=_to_camel, populate_by_name=True)


class AppointmentRead(AppointmentCreate):
    id: int
    model_config = ConfigDict(
        from_attributes=True, alias_generator=_to_camel, populate_by_name=True
    )


from sqlalchemy import Column, String, Integer
from app.db.schema import Base


class Appointments(Base):
    __tablename__ = "appointments"

    title = Column(String)
    with_person = Column(String)
    location = Column(String)
    date = Column(String)
    duration = Column(Integer)
    preparation_time = Column(Integer)
    notes = Column(String)
    id = Column(Integer)
