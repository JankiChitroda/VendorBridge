from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.models.approval import Approval
from app.models.quotation import Quotation

from app.schemas.approval import (
    ApprovalAction
)

router = APIRouter(
    prefix="/approvals",
    tags=["Approval Workflow"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{quotation_id}")
def create_approval(
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

    approval = Approval(
        quotation_id=quotation_id
    )

    db.add(approval)
    db.commit()
    db.refresh(approval)

    return approval

@router.put("/{approval_id}/approve")
def approve(
    approval_id: int,
    data: ApprovalAction,
    db: Session = Depends(get_db)
):

    approval = db.query(
        Approval
    ).filter(
        Approval.id == approval_id
    ).first()

    if not approval:
        raise HTTPException(
            status_code=404,
            detail="Approval not found"
        )

    approval.status = "approved"
    approval.remarks = data.remarks

    db.commit()

    return {
        "message": "Approved"
    }

@router.put("/{approval_id}/reject")
def reject(
    approval_id: int,
    data: ApprovalAction,
    db: Session = Depends(get_db)
):

    approval = db.query(
        Approval
    ).filter(
        Approval.id == approval_id
    ).first()

    if not approval:
        raise HTTPException(
            status_code=404,
            detail="Approval not found"
        )

    approval.status = "rejected"
    approval.remarks = data.remarks

    db.commit()

    return {
        "message": "Rejected"
    }

@router.get("/{approval_id}")
def get_status(
    approval_id: int,
    db: Session = Depends(get_db)
):

    approval = db.query(
        Approval
    ).filter(
        Approval.id == approval_id
    ).first()

    if not approval:
        raise HTTPException(
            status_code=404,
            detail="Approval not found"
        )

    return approval
@router.get("/")
def approval_history(
    db: Session = Depends(get_db)
):
    return db.query(
        Approval
    ).order_by(
        Approval.created_at.desc()
    ).all()