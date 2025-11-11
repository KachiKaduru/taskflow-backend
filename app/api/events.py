from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.auth import get_current_user
from app.db.schema import db_dependency
from app.models.events import Event, EventCreate, EventRead

router = APIRouter(prefix="/events", tags=["Events"])

user_dependency = Annotated[dict, Depends(get_current_user)]


# CREATE
@router.post("/create", response_model=EventRead, status_code=status.HTTP_201_CREATED)
async def create_event(event: EventCreate, db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    db_event = Event(**event.model_dump(), user_id=user["id"])

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return db_event


# READ
@router.get("/all", response_model=List[EventRead], status_code=status.HTTP_200_OK)
async def get_all_events(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    events = db.query(Event).filter(Event.user_id == user["id"]).all()

    return events


@router.get("/{event_id}", response_model=EventRead, status_code=status.HTTP_200_OK)
async def get_single_event(event_id: str, db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    event = (
        db.query(Event)
        .filter(Event.user_id == user["id"])
        .filter(Event.event_id == event_id)
        .first()
    )

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return event


# UPDATE
@router.put("/update/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_event(
    event_id: str,
    updated_event: EventCreate,
    db: db_dependency,
    user: user_dependency,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    event = (
        db.query(Event)
        .filter(Event.user_id == user["id"])
        .filter(Event.event_id == event_id)
        .first()
    )

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    for key, value in updated_event.model_dump().items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)


# DELETE
@router.delete("/delete/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: str, db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    event_model = (
        db.query(Event)
        .filter(Event.user_id == user["id"])
        .filter(Event.event_id == event_id)
        .first()
    )

    if event_model is None:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(event_model)
    db.commit()
