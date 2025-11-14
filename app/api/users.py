from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

user_dependency = Depends(get_current_user)


@router.get("/me")
async def read_current_user(user=user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user
