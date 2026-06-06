from pydantic import BaseModel, EmailStr


from typing import Literal

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Literal[
        "admin",
        "manager",
        "vendor",
        "procurement_officer"
    ]


class UserLogin(BaseModel):
    email: EmailStr
    password: str