from fastapi import FastAPI
from dotenv import load_dotenv

from app.db.schema import Base, engine
from app.api import appointments, events, tasks

from app.core import auth

app = FastAPI()

load_dotenv()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    # Ensure tables exist (SQLite for now). Importing models registers them on Base.


# Include routers
app.include_router(auth.router)
app.include_router(events.router)
app.include_router(tasks.router)
app.include_router(appointments.router)
