from typing import Annotated, List

from fastapi import APIRouter, Depends

from app.core.auth import get_current_user
from app.db.schema import db_dependency
from app.models.tasks import Task, TaskCreate, TaskRead

router = APIRouter(prefix="/tasks", tags=["Tasks"])

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/", response_model=TaskRead)
async def create_task(task: TaskCreate, db: db_dependency, user: user_dependency):
    data = task.model_dump()
    db_task = Task(**data, user_id=user["id"])
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/", response_model=List[TaskRead])
async def list_tasks(db: db_dependency, user: user_dependency):
    tasks = db.query(Task).filter(Task.user_id == user["id"]).all()
    return tasks
