from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.purchase_order import PurchaseOrder
from app.models.quotation import Quotation

router = APIRouter(
    prefix="/purchase-orders",
    tags=["Purchase Orders"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_po_number():
    return f"PO-{datetime.now().strftime('%Y%m%d%H%M%S')}"

@router.post("/create/{quotation_id}")
def create_po(
    quotation_id: int,
    db: Session = Depends(get_db)
):
    ...