from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.auth import get_current_user
from app.db.schema import db_dependency

router = APIRouter(prefix="/users", tags=["Users"])
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/me")
async def read_current_user(user: user_dependency):
    return user
