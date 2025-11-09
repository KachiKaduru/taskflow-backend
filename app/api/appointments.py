from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.schema import get_db
from app.models.appointments import Appointment, AppointmentCreate, AppointmentRead

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("/", response_model=AppointmentRead)
def create_appointment(
    appt: AppointmentCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    data = appt.model_dump()
    db_appt = Appointment(**data, user_id=user["id"])
    db.add(db_appt)
    db.commit()
    db.refresh(db_appt)
    return db_appt


@router.get("/", response_model=List[AppointmentRead])
def list_appointments(db: Session = Depends(get_db), user=Depends(get_current_user)):
    appts = db.query(Appointment).filter(Appointment.user_id == user["id"]).all()
    return appts
