from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    ForeignKey
)

from app.database import Base


class Quotation(Base):
    __tablename__ = "quotations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    rfq_id = Column(
        Integer,
        ForeignKey("rfqs.id")
    )

    vendor_id = Column(
        Integer,
        ForeignKey("vendors.id")
    )

    price = Column(
        Float,
        nullable=False
    )

    delivery_days = Column(
        Integer,
        nullable=False
    )

    notes = Column(String)

    status = Column(
        String,
        default="draft"
    )