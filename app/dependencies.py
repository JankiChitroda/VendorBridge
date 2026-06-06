from jose import jwt
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPBearer

from app.utils.security import (
    SECRET_KEY,
    ALGORITHM
)

security = HTTPBearer()


def get_current_user(
    token=Depends(security)
):
    try:
        payload = jwt.decode(
            token.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )