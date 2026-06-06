from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.models.rfq import RFQ
from app.models.vendor import Vendor
from app.models.quotation import Quotation

from app.schemas.quotation import (
    QuotationCreate,
    QuotationUpdate
)

router = APIRouter(
    prefix="/quotations",
    tags=["Quotation Management"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def submit_quotation(
    quotation: QuotationCreate,
    db: Session = Depends(get_db)
):

    rfq = db.query(RFQ).filter(
        RFQ.id == quotation.rfq_id
    ).first()

    if not rfq:
        raise HTTPException(
            status_code=404,
            detail="RFQ not found"
        )

    vendor = db.query(Vendor).filter(
        Vendor.id == quotation.vendor_id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    new_quotation = Quotation(
        **quotation.dict()
    )

    db.add(new_quotation)
    db.commit()
    db.refresh(new_quotation)

    return new_quotation

@router.get("/")
def get_quotations(
    db: Session = Depends(get_db)
):
    return db.query(Quotation).all()

@router.get("/{quotation_id}")
def get_quotation(
    quotation_id: int,
    db: Session = Depends(get_db)
):

    quotation = db.query(
        Quotation
    ).filter(
        Quotation.id == quotation_id
    ).first()

    if not quotation:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found"
        )

    return quotation

@router.put("/{quotation_id}")
def update_quotation(
    quotation_id: int,
    quotation_data: QuotationUpdate,
    db: Session = Depends(get_db)
):

    quotation = db.query(
        Quotation
    ).filter(
        Quotation.id == quotation_id
    ).first()

    if not quotation:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found"
        )

    quotation.price = quotation_data.price
    quotation.delivery_days = quotation_data.delivery_days
    quotation.notes = quotation_data.notes
    quotation.status = quotation_data.status

    db.commit()
    db.refresh(quotation)

    return quotation

@router.delete("/{quotation_id}")
def delete_quotation(
    quotation_id: int,
    db: Session = Depends(get_db)
):

    quotation = db.query(
        Quotation
    ).filter(
        Quotation.id == quotation_id
    ).first()

    if not quotation:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found"
        )

    db.delete(quotation)
    db.commit()

    return {
        "message": "Quotation deleted"
    }

@router.get("/compare/{rfq_id}")
def compare_quotations(
    rfq_id: int,
    db: Session = Depends(get_db)
):
    quotations = (
        db.query(Quotation)
        .filter(Quotation.rfq_id == rfq_id)
        .order_by(Quotation.price)
        .all()
    )

    return quotations

@router.put("/{quotation_id}/approve")
def approve_quotation(
    quotation_id: int,
    db: Session = Depends(get_db)
):
    quotation = (
        db.query(Quotation)
        .filter(
            Quotation.id == quotation_id
        )
        .first()
    )

    if not quotation:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found"
        )

    quotation.approved = True

    db.commit()
    db.refresh(quotation)

    return {
        "message": "Quotation approved"
    }

@router.get("/approved/{rfq_id}")
def approved_quotation(
    rfq_id: int,
    db: Session = Depends(get_db)
):

    quotation = (
        db.query(Quotation)
        .filter(
            Quotation.rfq_id == rfq_id,
            Quotation.approved == True
        )
        .first()
    )

    return quotation