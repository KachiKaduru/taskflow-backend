from app.db.schema import Base
from sqlalchemy import Column, String, Integer


class Appointments(Base):
    __tablename__ = "appointments"

    title = Column(String)
    with_person = Column(String)
    location = Column(String)
    date = Column(String)
    duration = Column(Integer)
    preparation_time = Column(Integer)
    notes = Column(String)
    id = Column(Integer)
