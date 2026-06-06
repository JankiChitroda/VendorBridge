
from pydantic import BaseModel


class ApprovalAction(BaseModel):
    remarks: str | None = None


class ApprovalResponse(BaseModel):
    id: int
    quotation_id: int
    status: str
    remarks: str | None

    class Config:
        from_attributes = True