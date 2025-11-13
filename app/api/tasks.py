from typing import Annotated, List
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.auth import get_current_user
from app.db.schema import db_dependency
from app.models.tasks import Task, TaskCreate, TaskRead

router = APIRouter(prefix="/tasks", tags=["Tasks"])

user_dependency = Depends(get_current_user)


# CREATE
@router.post("/create", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, db: db_dependency, user=user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    task_data = task.model_dump()
    task_data["user_id"] = user["id"]
    task_data["created_at"] = datetime.now(timezone.utc)
    task_data["updated_at"] = datetime.now(timezone.utc)
    db_task = Task(**task_data)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


# READ
@router.get("/all", response_model=List[TaskRead], status_code=status.HTTP_200_OK)
async def get_all_tasks(db: db_dependency, user=user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    tasks = db.query(Task).filter(Task.user_id == user.get("id")).all()
    return tasks


@router.get("/{task_id}", response_model=TaskRead, status_code=status.HTTP_200_OK)
async def get_single_task(task_id: str, db: db_dependency, user=user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    task = (
        db.query(Task)
        .filter(Task.user_id == user.get("id"))
        .filter(Task.id == task_id)
        .first()
    )

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# UPDATE
@router.put("/update/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_task(
    task_id: str,
    updated_task: TaskCreate,
    db: db_dependency,
    user=user_dependency,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    task = (
        db.query(Task)
        .filter(Task.user_id == user["id"])
        .filter(Task.id == task_id)
        .first()
    )

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_task_data = updated_task.model_dump()
    updated_task_data["updated_at"] = datetime.now(timezone.utc)

    for key, value in updated_task_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)


# DELETE
@router.delete("/delete/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, db: db_dependency, user=user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    task_model = (
        db.query(Task)
        .filter(Task.user_id == user["id"])
        .filter(Task.id == task_id)
        .first()
    )

    if task_model is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task_model)
    db.commit()
