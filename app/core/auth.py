from datetime import timedelta, datetime, timezone
import datetime
import os
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError

from app.db.schema import db_dependency
from app.models.users import Users, UsersCreate, UsersRead

# SECRET_KEY=f416585b384264a566bcd1158680145ee6e9c8c060dabae31b4352e1fc0d5eb5

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError(
        "SECRET_KEY environment variable is not set. Please check your .env file."
    )
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(prefix="/auth", tags=["Authentication"])


def create_access_token(id: str, name: str, email: str, expires_in: timedelta) -> str:
    expires = datetime.datetime.now(timezone.utc) + expires_in

    encoded = {"id": id, "name": name, "email": email, "exp": expires}
    token = jwt.encode(encoded, SECRET_KEY, algorithm=ALGORITHM)

    return token


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {
            "id": user_id,
            "name": payload.get("name"),
            "email": payload.get("email"),
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def authenticate_user(email: str, password: str, db) -> Users:
    user = db.query(Users).filter(Users.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not pwd_context.verify(password, str(user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


@router.post("/token", status_code=status.HTTP_200_OK)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
) -> dict:
    user = authenticate_user(form_data.username, form_data.password, db)

    access_token = create_access_token(
        id=str(user.id),
        name=str(user.name),
        email=str(user.email),
        expires_in=timedelta(hours=24),
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/create-user", status_code=status.HTTP_201_CREATED)
async def create_user(user: UsersCreate, db: db_dependency):
    existing_user = db.query(Users).filter(Users.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = pwd_context.hash(user.password)
    new_user = Users(
        name=user.name,
        email=user.email,
        image=user.image,
        hashed_password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


@router.get("/users", response_model=List[UsersRead], status_code=status.HTTP_200_OK)
async def get_users(db: db_dependency) -> List[Users]:
    users = db.query(Users).all()
    return users


@router.get(
    "/users/{user_id}", response_model=UsersRead, status_code=status.HTTP_200_OK
)
async def get_user(user_id: str, db: db_dependency) -> Users:
    user = db.query(Users).filter(Users.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user
