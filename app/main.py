from fastapi import FastAPI

from app.db.schema import Base, engine
from app.api import events as events_api  # type: ignore
from app.api import tasks as tasks_api  # type: ignore
from app.api import appointments as appts_api  # type: ignore


app = FastAPI()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    # Ensure tables exist (SQLite for now). Importing models registers them on Base.


# Include routers
app.include_router(events_api.router)
app.include_router(tasks_api.router)
app.include_router(appts_api.router)
