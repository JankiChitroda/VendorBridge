from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    po_number = Column(String, unique=True)

    quotation_id = Column(
        Integer,
        ForeignKey("quotations.id")
    )

    subtotal = Column(Float)
    tax_percent = Column(Float)
    tax_amount = Column(Float)
    total_amount = Column(Float)

    status = Column(
        String,
        default="generated"
    )