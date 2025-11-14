from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.db.schema import Base, engine
from app.api import appointments, events, tasks, users
from app.core import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions can be added here
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown actions can be added here


app = FastAPI(lifespan=lifespan)

# CORS middleware - Update origins with your frontend URLs
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://taskflow-inc.vercel.app",  # Your Vercel deployment
        # Add more origins as needed
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(events.router)
app.include_router(tasks.router)
app.include_router(appointments.router)
