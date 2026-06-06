from fastapi import FastAPI
from app.database import Base, engine
from app.models.user import User
from app.routes.auth import router as auth_router
from app.models.vendor import Vendor
from app.routes.vendor import router as vendor_router

from app.models.rfq import RFQ
from app.routes.rfq import router as rfq_router
from app.models.quotation import Quotation
from app.routes.quotation import (
    router as quotation_router
)
from app.routes.dashboard import (
    router as dashboard_router
)


from app.models.approval import Approval
from app.routes.approval import (
    router as approval_router
)
from app.routes.invoice import router as invoice_router

from app.models.invoice import Invoice
from app.routes.reports import (
    router as reports_router
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="VendorBridge API",
    version="1.0.0"
)

# Include Authentication Routes
@app.get("/")
def root():
    return {
        "message": "VendorBridge API Running"
    }



app.include_router(invoice_router)
app.include_router(auth_router)
app.include_router(vendor_router)
app.include_router(rfq_router)
app.include_router(
    quotation_router
)
app.include_router(
    approval_router
)

app.include_router(
    reports_router
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    dashboard_router
)