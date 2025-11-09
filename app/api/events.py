from typing import Annotated, List

from fastapi import APIRouter, Depends

from app.core.auth import get_current_user
from app.db.schema import db_dependency
from app.models.events import Event, EventCreate, EventRead

router = APIRouter(prefix="/events", tags=["Events"])

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/", response_model=EventRead)
async def create_event(event: EventCreate, db: db_dependency, user: user_dependency):
    data = event.model_dump()
    db_event = Event(**data, user_id=user["id"])
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@router.get("/", response_model=List[EventRead])
async def list_events(db: db_dependency, user: user_dependency):
    events = db.query(Event).filter(Event.user_id == user["id"]).all()
    return events
