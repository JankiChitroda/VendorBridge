from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from app.models.activity_log import ActivityLog
from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.models.rfq import RFQ
from app.models.vendor import Vendor

from app.schemas.rfq import (
    RFQCreate,
    RFQUpdate
)

router = APIRouter(
    prefix="/rfqs",
    tags=["RFQ Management"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_rfq(
    rfq: RFQCreate,
    db: Session = Depends(get_db)
):

    vendor = db.query(Vendor).filter(
        Vendor.id == rfq.vendor_id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    new_rfq = RFQ(
    title=rfq.title,
    description=rfq.description,
    quantity=rfq.quantity
)

    db.add(new_rfq)
    db.commit()
    db.refresh(new_rfq)

        # Activity Log
    log = ActivityLog(
            action="RFQ Created",
            description=f"RFQ '{new_rfq.title}' created",
            user_id=1
        )

    db.add(log)
    db.commit()

    return new_rfq

@router.get("/")
def get_rfqs(
    db: Session = Depends(get_db)
):
    return db.query(RFQ).all()

@router.get("/{rfq_id}")
def get_rfq(
    rfq_id: int,
    db: Session = Depends(get_db)
):

    rfq = db.query(RFQ).filter(
        RFQ.id == rfq_id
    ).first()

    if not rfq:
        raise HTTPException(
            status_code=404,
            detail="RFQ not found"
        )

    return rfq

@router.put("/{rfq_id}")
def update_rfq(
    rfq_id: int,
    rfq_data: RFQUpdate,
    db: Session = Depends(get_db)
):

    rfq = db.query(RFQ).filter(
        RFQ.id == rfq_id
    ).first()

    if not rfq:
        raise HTTPException(
            status_code=404,
            detail="RFQ not found"
        )

    for key, value in rfq_data.dict().items():
        setattr(rfq, key, value)

    db.commit()
    db.refresh(rfq)

    return rfq

@router.delete("/{rfq_id}")
def delete_rfq(
    rfq_id: int,
    db: Session = Depends(get_db)
):

    rfq = db.query(RFQ).filter(
        RFQ.id == rfq_id
    ).first()

    if not rfq:
        raise HTTPException(
            status_code=404,
            detail="RFQ not found"
        )

    db.delete(rfq)
    db.commit()

    return {
        "message": "RFQ deleted"
    }

