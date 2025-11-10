from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.auth import get_current_user
from app.db.schema import db_dependency
from app.models.appointments import Appointment, AppointmentCreate, AppointmentRead

router = APIRouter(prefix="/appointments", tags=["Appointments"])

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post(
    "/create", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED
)
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


@router.get(
    "/all", response_model=List[AppointmentRead], status_code=status.HTTP_200_OK
)
async def get_all_appointments(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    appts = db.query(Appointment).filter(Appointment.user_id == user["id"]).all()

    return appts


@router.get(
    "/{appt_id}", response_model=AppointmentRead, status_code=status.HTTP_200_OK
)
async def get_single_appointment(
    appt_id: str, db: db_dependency, user: user_dependency
):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    appointment = (
        db.query(Appointment)
        .filter(Appointment.user_id == user["id"])
        .filter(Appointment.appt_id == appt_id)
        .first()
    )

    return appointment
