from strands import tool
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.tables import RentPayment, Tenant, Room


class FinanceTools:
    """Tools for financial operations (rent, payments)."""

    def __init__(self, session_factory):
        self.session_factory = session_factory

    @tool
    def get_pending_rent(self) -> dict:
        """Get all pending and overdue rent payments.

        Returns:
            List of pending/overdue payments with tenant details.
        """
        db = self.session_factory()
        try:
            payments = db.query(RentPayment).filter(
                RentPayment.status.in_(["PENDING", "OVERDUE"])
            ).order_by(RentPayment.due_date).all()

            result = []
            for p in payments:
                tenant = db.query(Tenant).filter(Tenant.id == p.tenant_id).first()
                room = db.query(Room).filter(Room.id == tenant.room_id).first() if tenant and tenant.room_id else None
                result.append({
                    "id": p.id,
                    "tenant_id": p.tenant_id,
                    "tenant_name": tenant.name if tenant else "Unknown",
                    "tenant_phone": tenant.phone if tenant else None,
                    "room_number": room.room_number if room else None,
                    "amount": float(p.amount),
                    "due_date": str(p.due_date),
                    "status": p.status,
                })

            return {
                "status": "success",
                "payments": result,
                "total_pending": sum(p["amount"] for p in result),
            }
        finally:
            db.close()

    @tool
    def get_rent_status(self, tenant_id: int) -> dict:
        """Get rent payment status for a specific tenant.

        Args:
            tenant_id: The tenant's ID.

        Returns:
            Rent payment history and current status.
        """
        db = self.session_factory()
        try:
            payments = db.query(RentPayment).filter(
                RentPayment.tenant_id == tenant_id
            ).order_by(RentPayment.due_date.desc()).all()

            tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
            room = db.query(Room).filter(Room.id == tenant.room_id).first() if tenant and tenant.room_id else None

            return {
                "status": "success",
                "tenant": {
                    "id": tenant.id if tenant else None,
                    "name": tenant.name if tenant else None,
                    "room_number": room.room_number if room else None,
                },
                "payments": [
                    {
                        "id": p.id,
                        "amount": float(p.amount),
                        "due_date": str(p.due_date),
                        "paid_date": str(p.paid_date) if p.paid_date else None,
                        "status": p.status,
                        "payment_method": p.payment_method,
                    }
                    for p in payments
                ],
                "total_due": sum(float(p.amount) for p in payments if p.status in ["PENDING", "OVERDUE"]),
            }
        finally:
            db.close()
