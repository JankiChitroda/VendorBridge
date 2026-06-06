from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate, VendorUpdate

router = APIRouter(
    prefix="/vendors",
    tags=["Vendor Management"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_vendor(
    vendor: VendorCreate,
    db: Session = Depends(get_db)
):

    existing_vendor = db.query(Vendor).filter(
        Vendor.gst_number == vendor.gst_number
    ).first()

    if existing_vendor:
        raise HTTPException(
            status_code=400,
            detail="Vendor already exists"
        )
    if vendor.status not in ["active", "inactive", "pending"]:
        raise HTTPException(
        status_code=400,
        detail="Status must be active, inactive, or pending"
    )

    new_vendor = Vendor(**vendor.dict())

    db.add(new_vendor)
    db.commit()
    db.refresh(new_vendor)

    return new_vendor

@router.get("/")
def get_all_vendors(
    db: Session = Depends(get_db)
):
    return db.query(Vendor).all()

@router.get("/{vendor_id}")
def get_vendor(
    vendor_id: int,
    db: Session = Depends(get_db)
):

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    return vendor

@router.put("/{vendor_id}")
def update_vendor(
    vendor_id: int,
    vendor_data: VendorUpdate,
    db: Session = Depends(get_db)
):

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    for key, value in vendor_data.dict().items():
        setattr(vendor, key, value)

    db.commit()
    db.refresh(vendor)

    return vendor

@router.delete("/{vendor_id}")
def delete_vendor(
    vendor_id: int,
    db: Session = Depends(get_db)
):

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    db.delete(vendor)
    db.commit()

    return {
        "message": "Vendor deleted successfully"
    }

@router.patch("/{vendor_id}/status")
def update_status(
    vendor_id: int,
    status: str,
    db: Session = Depends(get_db)
):

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    vendor.status = status

    db.commit()

    return {
        "message": "Status updated"
    }

@router.get("/search/")
def search_vendor(
    name: str,
    db: Session = Depends(get_db)
):

    vendors = db.query(Vendor).filter(
        Vendor.vendor_name.contains(name)
    ).all()

    return vendors

@router.get("/filter/category")
def filter_category(
    category: str,
    db: Session = Depends(get_db)
):

    return db.query(Vendor).filter(
        Vendor.category == category
    ).all()

@router.get("/filter/status")
def filter_status(
    status: str,
    db: Session = Depends(get_db)
):

    return db.query(Vendor).filter(
        Vendor.status == status
    ).all()