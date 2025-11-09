from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.schema import get_db
from app.models.events import Event, EventCreate, EventRead

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventRead)
def create_event(
    event: EventCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    data = event.model_dump()
    db_event = Event(**data, user_id=user["id"])
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@router.get("/", response_model=List[EventRead])
def list_events(db: Session = Depends(get_db), user=Depends(get_current_user)):
    events = db.query(Event).filter(Event.user_id == user["id"]).all()
    return events
