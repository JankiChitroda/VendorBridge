from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.utils.security import hash_password, verify_password
from app.utils.security import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from app.dependencies import get_current_user


@router.get("/me")
def get_me(
    current_user=Depends(get_current_user)
):
    return current_user

# SIGNUP ENDPOINT
@router.post("/signup")
def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role.lower()
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created successfully"}


# LOGIN ENDPOINT
@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
    {
        "user_id": db_user.id,
        "email": db_user.email,
        "role": db_user.role
    }
)

    return {
    "access_token": token,
    "token_type": "bearer",
    "role": db_user.role
}

from app.dependencies import get_current_user


@router.get("/protected")
def protected_route(
    current_user=Depends(get_current_user)
):
    return {
        "message": "Access granted",
        "user": current_user
    }

from app.utils.role_checker import require_roles


@router.get("/admin")
def admin_only(
    current_user=Depends(get_current_user)
):

    require_roles("admin")(current_user)

    return {
        "message": "Welcome Admin"
    }