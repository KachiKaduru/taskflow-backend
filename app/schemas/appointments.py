
from pydantic import BaseModel


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
*