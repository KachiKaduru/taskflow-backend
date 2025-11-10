from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.auth import get_current_user
from app.db.schema import db_dependency
from app.models.appointments import Appointment, AppointmentCreate, AppointmentRead

router = APIRouter(prefix="/appointments", tags=["Appointments"])

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    appt: AppointmentCreate,
    db: db_dependency,
    user: user_dependency,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    db_appt = Appointment(**appt.model_dump(), user_id=user["id"])
    db.add(db_appt)
    db.commit()
    db.refresh(db_appt)
    return db_appt


@router.get("/", response_model=List[AppointmentRead], status_code=status.HTTP_200_OK)
async def get_all_appointments(db: db_dependency, user: user_dependency):
    appts = db.query(Appointment).filter(Appointment.user_id == user["id"]).all()
    return appts


@router.get(
    "/{appointment_id}", response_model=AppointmentRead, status_code=status.HTTP_200_OK
)
async def get_single_appointment(
    appointment_id: int, db: db_dependency, user: user_dependency
):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    appointment = (
        db.query(Appointment)
        .filter(Appointment.user_id == user["id"])
        .filter(Appointment.id == appointment_id)
        .first()
    )

    return appointment
