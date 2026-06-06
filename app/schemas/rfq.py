from pydantic import BaseModel
from datetime import datetime


class RFQCreate(BaseModel):
    title: str
    product_details: str
    quantity: int
    attachment: str | None = None
    deadline: datetime
    vendor_id: int


class RFQUpdate(BaseModel):
    title: str
    product_details: str
    quantity: int
    attachment: str | None = None
    deadline: datetime
    vendor_id: int
    status: str