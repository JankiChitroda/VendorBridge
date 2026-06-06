from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.models.rfq import RFQ
from app.models.invoice import Invoice
from app.models.purchase_order import PurchaseOrder
from app.models.approval import Approval

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def dashboard_summary(
    db: Session = Depends(get_db)
):

    pending_approvals = (
        db.query(Approval)
        .filter(Approval.status == "pending")
        .count()
    )

    active_rfqs = db.query(RFQ).count()

    recent_purchase_orders = (
        db.query(PurchaseOrder)
        .order_by(PurchaseOrder.id.desc())
        .limit(5)
        .all()
    )

    recent_invoices = (
        db.query(Invoice)
        .order_by(Invoice.id.desc())
        .limit(5)
        .all()
    )

    return {
        "pending_approvals": pending_approvals,
        "active_rfqs": active_rfqs,
        "recent_purchase_orders": recent_purchase_orders,
        "recent_invoices": recent_invoices
    }

@router.get("/analytics")
def analytics_cards(
    db: Session = Depends(get_db)
):
    return {
        "total_rfqs": db.query(RFQ).count(),
        "total_pos": db.query(PurchaseOrder).count(),
        "total_invoices": db.query(Invoice).count(),
        "pending_approvals": db.query(Approval)
            .filter(Approval.status == "pending")
            .count()
    }