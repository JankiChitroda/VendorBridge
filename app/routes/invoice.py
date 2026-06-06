from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.invoice import Invoice
from app.models.purchase_order import PurchaseOrder

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Generate Invoice
@router.post("/{po_id}")
def generate_invoice(
    po_id: int,
    db: Session = Depends(get_db)
):
    po = db.query(
        PurchaseOrder
    ).filter(
        PurchaseOrder.id == po_id
    ).first()

    if not po:
        raise HTTPException(
            status_code=404,
            detail="Purchase Order not found"
        )

    invoice = Invoice(
        invoice_number=f"INV-{po.po_number}",
        po_id=po.id,
        subtotal=po.subtotal,
        tax_amount=po.tax_amount,
        total_amount=po.total_amount
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    return invoice


# Get Invoice
@router.get("/{invoice_id}")
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db)
):
    invoice = db.query(
        Invoice
    ).filter(
        Invoice.id == invoice_id
    ).first()

    if not invoice:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    return invoice


# Update Invoice Status
@router.put("/{invoice_id}/status")
def update_invoice_status(
    invoice_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    invoice = db.query(
        Invoice
    ).filter(
        Invoice.id == invoice_id
    ).first()

    if not invoice:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    invoice.status = status

    db.commit()
    db.refresh(invoice)

    return {
        "message": "Invoice status updated",
        "status": invoice.status
    }


# Get All Invoices
@router.get("/")
def get_all_invoices(
    db: Session = Depends(get_db)
):
    return db.query(
        Invoice
    ).all()