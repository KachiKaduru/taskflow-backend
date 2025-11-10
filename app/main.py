from fastapi import FastAPI
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from app.db.schema import Base, engine
from app.api import appointments, events, tasks
from app.core import auth

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions can be added here
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown actions can be added here


app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(auth.router)
app.include_router(events.router)
app.include_router(tasks.router)
app.include_router(appointments.router)
