from typing import Annotated, List

from fastapi import APIRouter, Depends

from app.core.auth import get_current_user
from app.db.schema import db_dependency
from app.models.appointments import Appointment, AppointmentCreate, AppointmentRead

router = APIRouter(prefix="/appointments", tags=["Appointments"])

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/", response_model=AppointmentRead)
async def create_appointment(
    appt: AppointmentCreate,
    db: db_dependency,
    user: user_dependency,
):
    data = appt.model_dump()
    db_appt = Appointment(**data, user_id=user["id"])
    db.add(db_appt)
    db.commit()
    db.refresh(db_appt)
    return db_appt


@router.get("/", response_model=List[AppointmentRead])
async def list_appointments(db: db_dependency, user: user_dependency):
    appts = db.query(Appointment).filter(Appointment.user_id == user["id"]).all()
    return appts
