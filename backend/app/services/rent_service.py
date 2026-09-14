"""
Rent Service - Automated rent generation, reminders, and overdue tracking.
"""

import logging
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.tables import Tenant, Room, RentPayment, Message, AgentAction

logger = logging.getLogger(__name__)


class RentService:
    def __init__(self, db: Session):
        self.db = db

    def generate_monthly_rent(self, month: int = None, year: int = None) -> dict:
        """Generate rent payments for all active tenants for a given month."""
        today = date.today()
        month = month or today.month
        year = year or today.year

        due_date = date(year, month, 5)

        tenants = self.db.query(Tenant).filter(Tenant.status == "ACTIVE").all()
        created = 0
        skipped = 0

        for tenant in tenants:
            existing = self.db.query(RentPayment).filter(
                RentPayment.tenant_id == tenant.id,
                RentPayment.due_date == due_date,
            ).first()

            if existing:
                skipped += 1
                continue

            room = self.db.query(Room).filter(Room.id == tenant.room_id).first()
            if not room:
                continue

            payment = RentPayment(
                tenant_id=tenant.id,
                amount=room.rent_amount,
                due_date=due_date,
                status="PENDING",
            )
            self.db.add(payment)
            created += 1

        self.db.commit()

        action = AgentAction(
            agent_name="rent_service",
            action_type="GENERATE_MONTHLY_RENT",
            input_data={"month": month, "year": year},
            output_data={"created": created, "skipped": skipped},
            status="SUCCESS",
            completed_at=datetime.now(),
        )
        self.db.add(action)
        self.db.commit()

        return {
            "status": "success",
            "month": month,
            "year": year,
            "created": created,
            "skipped": skipped,
        }

    def mark_overdue(self) -> dict:
        """Mark overdue rent payments."""
        today = date.today()
        overdue = self.db.query(RentPayment).filter(
            RentPayment.status == "PENDING",
            RentPayment.due_date < today,
        ).all()

        count = 0
        for payment in overdue:
            payment.status = "OVERDUE"
            count += 1

        self.db.commit()

        if count > 0:
            action = AgentAction(
                agent_name="rent_service",
                action_type="MARK_OVERDUE",
                input_data={"date": str(today)},
                output_data={"overdue_count": count},
                status="SUCCESS",
                completed_at=datetime.now(),
            )
            self.db.add(action)
            self.db.commit()

        return {"status": "success", "marked_overdue": count}

    def send_rent_reminders(self) -> dict:
        """Send rent reminders to tenants with pending payments."""
        pending = self.db.query(RentPayment).filter(
            RentPayment.status.in_(["PENDING", "OVERDUE"])
        ).all()

        sent = 0
        for payment in pending:
            tenant = self.db.query(Tenant).filter(Tenant.id == payment.tenant_id).first()
            if not tenant:
                continue

            days_until_due = (payment.due_date - date.today()).days
            if payment.status == "OVERDUE":
                msg_text = f"Hi {tenant.name}, your rent of ₹{payment.amount} is overdue. Please pay immediately."
            elif days_until_due <= 3:
                msg_text = f"Hi {tenant.name}, reminder: ₹{payment.amount} rent due on {payment.due_date}."
            else:
                continue

            message = Message(
                tenant_id=tenant.id,
                direction="OUTBOUND",
                channel="SYSTEM",
                message_type="TEXT",
                message_text=msg_text,
                processed=1,
            )
            self.db.add(message)
            sent += 1

        self.db.commit()

        action = AgentAction(
            agent_name="rent_service",
            action_type="SEND_RENT_REMINDERS",
            output_data={"reminders_sent": sent},
            status="SUCCESS",
            completed_at=datetime.now(),
        )
        self.db.add(action)
        self.db.commit()

        return {"status": "success", "reminders_sent": sent}

    def get_rent_summary(self) -> dict:
        """Get comprehensive rent summary."""
        total_expected = self.db.query(func.sum(RentPayment.amount)).scalar() or 0
        total_paid = self.db.query(func.sum(RentPayment.amount)).filter(RentPayment.status == "PAID").scalar() or 0
        total_pending = self.db.query(func.sum(RentPayment.amount)).filter(RentPayment.status == "PENDING").scalar() or 0
        total_overdue = self.db.query(func.sum(RentPayment.amount)).filter(RentPayment.status == "OVERDUE").scalar() or 0

        return {
            "total_expected": float(total_expected),
            "total_paid": float(total_paid),
            "total_pending": float(total_pending),
            "total_overdue": float(total_overdue),
            "collection_rate": round(total_paid / total_expected * 100, 1) if total_expected > 0 else 0,
        }
