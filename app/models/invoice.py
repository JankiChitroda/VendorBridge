from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    invoice_number = Column(
        String,
        unique=True
    )

    po_id = Column(
        Integer,
        ForeignKey("purchase_orders.id")
    )

    subtotal = Column(Float)
    tax_amount = Column(Float)
    total_amount = Column(Float)

    status = Column(
        String,
        default="pending"
    )