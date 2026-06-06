from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.activity_log import ActivityLog
from app.schemas.activity_log import ActivityLogCreate

router = APIRouter(
    prefix="/activity-logs",
    tags=["Activity Logs"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_log(
    log: ActivityLogCreate,
    db: Session = Depends(get_db)
):

    new_log = ActivityLog(
        action=log.action,
        description=log.description,
        user_id=log.user_id
    )

    db.add(new_log)
    db.commit()

    return {
        "message": "Activity logged"
    }

@router.get("/")
def get_activity_timeline(
    db: Session = Depends(get_db)
):

    return db.query(
        ActivityLog
    ).order_by(
        ActivityLog.created_at.desc()
    ).all()

@router.get("/user/{user_id}")
def get_user_logs(
    user_id: int,
    db: Session = Depends(get_db)
):

    return db.query(
        ActivityLog
    ).filter(
        ActivityLog.user_id == user_id
    ).all()