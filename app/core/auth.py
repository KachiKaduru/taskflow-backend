import os
from typing import Optional

from fastapi import Depends, Header, HTTPException, status

import jwt

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def create_access_token(subject: str) -> str:
    """Create a simple JWT with the subject (user id or identifier).

    This is a tiny helper for tests. In production use stronger signing and expirations.
    """
    token = jwt.encode({"sub": str(subject)}, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_current_user(
    authorization: Optional[str] = Header(None), x_user_id: Optional[str] = Header(None)
):
    """Very small auth stub.

    Supports passing a JWT in the Authorization header (Bearer <token>), or an X-User-Id header
    for quick local testing. Returns a dict with at least `id` key.
    """
    # Quick path: allow X-User-Id for dev convenience
    if x_user_id:
        try:
            return {"id": int(x_user_id)}
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid X-User-Id header",
            )

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
        )

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header",
        )

    token = parts[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if not sub:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
            )
        return {"id": int(sub)}
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
