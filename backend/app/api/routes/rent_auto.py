"""
Rent Automation API - Generate rent, send reminders, track overdue.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ...services.rent_service import RentService

router = APIRouter()


@router.post("/generate")
def generate_rent(db: Session = Depends(get_db)):
    """Generate monthly rent payments for all active tenants."""
    service = RentService(db)
    return service.generate_monthly_rent()


@router.post("/mark-overdue")
def mark_overdue(db: Session = Depends(get_db)):
    """Mark overdue rent payments."""
    service = RentService(db)
    return service.mark_overdue()


@router.post("/send-reminders")
def send_reminders(db: Session = Depends(get_db)):
    """Send rent reminders to tenants with pending payments."""
    service = RentService(db)
    return service.send_rent_reminders()


@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    """Get comprehensive rent summary."""
    service = RentService(db)
    return service.get_rent_summary()
