from typing import Annotated, List

from fastapi import APIRouter, Depends
from starlette import status

from app.core.auth import get_current_user
from app.db.schema import db_dependency
from app.models.tasks import Task, TaskCreate, TaskRead

router = APIRouter(prefix="/tasks", tags=["Tasks"])

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    db_task = Task(**task.model_dump(), user_id=user["id"])

    db.add(db_task)
    db.commit()
    db.refresh(db_task)


@router.get("/", response_model=List[TaskRead], status_code=status.HTTP_200_OK)
async def list_tasks(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    tasks = db.query(Task).filter(Task.user_id == user["id"]).all()
    return tasks


@router.get("/{task_id}", response_model=TaskRead, status_code=status.HTTP_200_OK)
async def get_single_task(task_id: int, db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    task = (
        db.query(Task)
        .filter(Task.user_id == user["id"])
        .filter(Task.id == task_id)
        .first()
    )

    return task
