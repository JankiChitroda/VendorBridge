from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from datetime import datetime
from app.database import Base
from pydantic import BaseModel


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    action = Column(String)

    description = Column(String)

    user_id = Column(Integer)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

