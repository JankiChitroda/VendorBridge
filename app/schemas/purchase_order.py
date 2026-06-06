from pydantic import BaseModel

class PurchaseOrderResponse(BaseModel):
    id: int
    po_number: str

    class Config:
        from_attributes = True