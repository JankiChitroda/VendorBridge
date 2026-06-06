from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from app.database import Base


class RFQ(Base):
    __tablename__ = "rfqs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    product_details = Column(
        String,
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    attachment = Column(String)

    deadline = Column(DateTime)

    vendor_id = Column(
        Integer,
        ForeignKey("vendors.id")
    )

    status = Column(
        String,
        default="draft"
    )