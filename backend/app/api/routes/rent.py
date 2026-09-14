from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from ...database import get_db
from ...models.tables import RentPayment, Tenant
from ...schemas.schemas import RentPaymentResponse, RentPaymentWithTenant, RentSummary, TenantBrief

router = APIRouter()


@router.get("/summary", response_model=RentSummary)
def get_rent_summary(db: Session = Depends(get_db)):
    total_expected = db.query(func.sum(RentPayment.amount)).scalar() or 0
    total_paid = db.query(func.sum(RentPayment.amount)).filter(RentPayment.status == "PAID").scalar() or 0
    total_pending = db.query(func.sum(RentPayment.amount)).filter(RentPayment.status == "PENDING").scalar() or 0
    total_overdue = db.query(func.sum(RentPayment.amount)).filter(RentPayment.status == "OVERDUE").scalar() or 0

    paid_count = db.query(func.count(RentPayment.id)).filter(RentPayment.status == "PAID").scalar() or 0
    pending_count = db.query(func.count(RentPayment.id)).filter(RentPayment.status == "PENDING").scalar() or 0
    overdue_count = db.query(func.count(RentPayment.id)).filter(RentPayment.status == "OVERDUE").scalar() or 0

    return RentSummary(
        total_expected=float(total_expected),
        total_paid=float(total_paid),
        total_pending=float(total_pending),
        total_overdue=float(total_overdue),
        paid_count=paid_count,
        pending_count=pending_count,
        overdue_count=overdue_count,
    )


@router.get("/payments", response_model=list[RentPaymentWithTenant])
def list_payments(db: Session = Depends(get_db)):
    payments = db.query(RentPayment).order_by(RentPayment.due_date.desc()).all()
    result = []
    for p in payments:
        payment_data = RentPaymentWithTenant.model_validate(p)
        tenant = db.query(Tenant).filter(Tenant.id == p.tenant_id).first()
        if tenant:
            payment_data.tenant = TenantBrief.model_validate(tenant)
        result.append(payment_data)
    return result
