from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from datetime import datetime
from app.database import Base


class Approval(Base):
    __tablename__ = "approvals"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    quotation_id = Column(
        Integer,
        ForeignKey("quotations.id")
    )

    status = Column(
        String,
        default="pending"
    )

    remarks = Column(String)

    approved_by = Column(
        Integer,
        ForeignKey("users.id")
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )