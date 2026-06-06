from pydantic import BaseModel
from sqlalchemy import Boolean,Column

approved = Column(Boolean, default=False)
class QuotationCreate(BaseModel):
    rfq_id: int
    vendor_id: int
    price: float
    delivery_days: int
    notes: str | None = None


class QuotationUpdate(BaseModel):
    price: float
    delivery_days: int
    notes: str | None = None
    status: str

class QuotationApproval(BaseModel):
    approved: bool

