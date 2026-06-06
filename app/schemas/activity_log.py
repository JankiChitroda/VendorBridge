from pydantic import BaseModel


class ActivityLogCreate(BaseModel):
    action: str
    description: str
    user_id: int