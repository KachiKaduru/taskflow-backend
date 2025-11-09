from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.db.schema import Base


def _to_camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(p.title() for p in parts[1:])


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime(timezone=False), nullable=True)
    created_at = Column(DateTime(timezone=False), nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    is_priority = Column(Boolean, default=False, nullable=False)
    is_recurring = Column(Boolean, default=False, nullable=False)
    recurrence_days = Column(Integer, nullable=True)

    def __repr__(self) -> str:  # pragma: no cover - tiny helper
        return f"<Task id={self.id} title={self.title!r}>"


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    created_at: datetime
    is_completed: bool = False
    is_priority: bool = False
    is_recurring: bool = False
    recurrence_days: Optional[int] = None

    model_config = ConfigDict(alias_generator=_to_camel, populate_by_name=True)


class TaskRead(TaskCreate):
    id: int
    model_config = ConfigDict(
        from_attributes=True, alias_generator=_to_camel, populate_by_name=True
    )
