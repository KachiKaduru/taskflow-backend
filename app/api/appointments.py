from typing import Annotated, List
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.auth import get_current_user
from app.db.schema import db_dependency
from app.models.appointments import Appointment, AppointmentCreate, AppointmentRead

router = APIRouter(prefix="/appointments", tags=["Appointments"])

user_dependency = Depends(get_current_user)


@router.post(
    "/create", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED
)
async def create_appointment(
    appt: AppointmentCreate,
    db: db_dependency,
    user=user_dependency,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    appt_data = appt.model_dump()
    appt_data["user_id"] = user["id"]
    appt_data["created_at"] = datetime.now(timezone.utc)
    appt_data["updated_at"] = datetime.now(timezone.utc)

    db_appt = Appointment(**appt_data)

    db.add(db_appt)
    db.commit()
    db.refresh(db_appt)

    return db_appt


@router.get(
    "/all", response_model=List[AppointmentRead], status_code=status.HTTP_200_OK
)
async def get_all_appointments(db: db_dependency, user=user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    appts = db.query(Appointment).filter(Appointment.user_id == user["id"]).all()

    return appts


@router.get(
    "/{appt_id}", response_model=AppointmentRead, status_code=status.HTTP_200_OK
)
async def get_single_appointment(appt_id: str, db: db_dependency, user=user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    appointment = (
        db.query(Appointment)
        .filter(Appointment.user_id == user["id"])
        .filter(Appointment.id == appt_id)
        .first()
    )

    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return appointment


@router.put("/update/{appt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_appointment(
    appt_id: str,
    updated_appt: AppointmentCreate,
    db: db_dependency,
    user=user_dependency,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    appointment_model = (
        db.query(Appointment)
        .filter(Appointment.user_id == user["id"])
        .filter(Appointment.id == appt_id)
        .first()
    )

    if appointment_model is None:
        raise HTTPException(status_code=404, detail="Appointment not found")

    updated_appt_data = updated_appt.model_dump()
    updated_appt_data["updated_at"] = datetime.now(timezone.utc)

    for key, value in updated_appt_data.items():
        setattr(appointment_model, key, value)

    db.commit()
    db.refresh(appointment_model)


@router.delete("/delete/{appt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(appt_id: str, db: db_dependency, user=user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    appointment_model = (
        db.query(Appointment)
        .filter(Appointment.user_id == user["id"])
        .filter(Appointment.id == appt_id)
        .first()
    )

    if appointment_model is None:
        raise HTTPException(status_code=404, detail="Appointment not found")

    db.delete(appointment_model)
    db.commit()
