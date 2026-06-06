from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import SessionLocal

from app.models.vendor import Vendor
from app.models.rfq import RFQ
from app.models.quotation import Quotation
from app.models.purchase_order import PurchaseOrder
from app.models.invoice import Invoice

import pandas as pd
from fastapi.responses import FileResponse

router = APIRouter(
    prefix="/reports",
    tags=["Reports & Analytics"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/statistics")
def procurement_statistics(
    db: Session = Depends(get_db)
):
    return {
        "vendors": db.query(Vendor).count(),
        "rfqs": db.query(RFQ).count(),
        "quotations": db.query(Quotation).count(),
        "purchase_orders": db.query(PurchaseOrder).count(),
        "invoices": db.query(Invoice).count()
    }

@router.get("/spending")
def spending_summary(
    db: Session = Depends(get_db)
):

    total_spending = db.query(
        func.sum(
            Invoice.total_amount
        )
    ).scalar()

    return {
        "total_spending": total_spending or 0
    }

@router.get("/vendor-performance")
def vendor_performance(
    db: Session = Depends(get_db)
):

    vendors = db.query(Vendor).all()

    result = []

    for vendor in vendors:

        result.append({
            "vendor_id": vendor.id,
            "vendor_name": vendor.name,
            "status": vendor.status
        })

    return result

@router.get("/monthly-trends")
def monthly_trends(
    db: Session = Depends(get_db)
):

    invoices = db.query(
        Invoice
    ).all()

    trends = {}

    for invoice in invoices:

        month = invoice.id

        if month not in trends:
            trends[month] = 0

        trends[month] += invoice.total_amount

    return trends

@router.get("/export")
def export_report(
    db: Session = Depends(get_db)
):

    invoices = db.query(
        Invoice
    ).all()

    data = []

    for invoice in invoices:

        data.append({
            "Invoice": invoice.invoice_number,
            "Total": invoice.total_amount,
            "Status": invoice.status
        })

    df = pd.DataFrame(data)

    filename = "report.xlsx"

    df.to_excel(
        filename,
        index=False
    )

    return FileResponse(
        filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename
    )