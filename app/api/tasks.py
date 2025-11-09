from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.schema import get_db
from app.models.tasks import Task, TaskCreate, TaskRead

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskRead)
def create_task(
    task: TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    data = task.model_dump()
    db_task = Task(**data, user_id=user["id"])
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/", response_model=List[TaskRead])
def list_tasks(db: Session = Depends(get_db), user=Depends(get_current_user)):
    tasks = db.query(Task).filter(Task.user_id == user["id"]).all()
    return tasks
