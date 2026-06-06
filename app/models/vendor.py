from sqlalchemy import Column, Integer, String
from app.database import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)

    vendor_name = Column(String, nullable=False)

    category = Column(String, nullable=False)

    gst_number = Column(
        String,
        unique=True,
        nullable=False
    )

    contact_person = Column(String)

    email = Column(String, nullable=False)

    phone = Column(String, nullable=False)

    address = Column(String)

    status = Column(
        String,
        default="pending"
    )