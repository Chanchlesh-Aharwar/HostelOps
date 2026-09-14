from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ...database import get_db
from ...models.tables import Vendor
from ...schemas.schemas import VendorResponse

router = APIRouter()


@router.get("/", response_model=list[VendorResponse])
def list_vendors(
    db: Session = Depends(get_db),
    category: str = Query(default=None),
    availability: str = Query(default=None),
):
    query = db.query(Vendor).filter(Vendor.status == "ACTIVE")
    if category:
        query = query.filter(Vendor.category == category.upper())
    if availability:
        query = query.filter(Vendor.availability == availability.upper())
    vendors = query.order_by(Vendor.rating.desc()).all()
    return [VendorResponse.model_validate(v) for v in vendors]


@router.get("/{vendor_id}", response_model=VendorResponse)
def get_vendor(vendor_id: int, db: Session = Depends(get_db)):
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return VendorResponse.model_validate(vendor)
