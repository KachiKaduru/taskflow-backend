from datetime import datetime, timezone
from typing import Optional
import uuid

from pydantic import BaseModel, ConfigDict, field_serializer
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, ForeignKey

from app.db.schema import Base
from app.core.utils.helpers import to_camel_case


class Task(Base):
    __tablename__ = "tasks"

    id = Column[str](
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    user_id = Column[str](String(36), ForeignKey("users.id"), nullable=True, index=True)

    title = Column[str](String(255), nullable=False)
    description = Column[str](Text, nullable=True)
    due_date = Column[datetime](DateTime(timezone=False), nullable=True)
    is_completed = Column[bool](Boolean, default=False, nullable=False)
    is_priority = Column[bool](Boolean, default=False, nullable=False)
    is_recurring = Column[bool](Boolean, default=False, nullable=False)
    recurrence_days = Column[int](Integer, nullable=True)
    status = Column[str](
        String(50), nullable=True
    )  # e.g., "pending", "in_progress", "completed"
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
        return f"<Task id={self.id} title={self.title!r}>"


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    is_completed: bool = False
    is_priority: bool = False
    is_recurring: bool = False
    recurrence_days: Optional[int] = None
    status: Optional[str] = None

    model_config = ConfigDict(alias_generator=to_camel_case, populate_by_name=True)


class TaskRead(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    is_completed: bool = False
    is_priority: bool = False
    is_recurring: bool = False
    recurrence_days: Optional[int] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    user_id: Optional[str] = None

    @field_serializer("due_date", "created_at", "updated_at", when_used="json")
    def serialize_datetime(self, value: Optional[datetime], _info) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.isoformat()
        return str(value)

    model_config = ConfigDict(
        from_attributes=True, alias_generator=to_camel_case, populate_by_name=True
    )
