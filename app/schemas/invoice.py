from pydantic import BaseModel

class InvoiceResponse(BaseModel):
    id: int
    invoice_number: str

    class Config:
        from_attributes = True