from pydantic import BaseModel, EmailStr


class VendorCreate(BaseModel):
    vendor_name: str
    category: str
    gst_number: str
    contact_person: str
    email: EmailStr
    phone: str
    address: str
    status: str

class VendorUpdate(BaseModel):
    vendor_name: str
    category: str
    gst_number: str
    contact_person: str
    email: EmailStr
    phone: str
    address: str
    status: str