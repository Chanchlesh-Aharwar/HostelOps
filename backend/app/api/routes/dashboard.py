from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from ...database import get_db
from ...models.tables import Room, Tenant, Vendor, Complaint, RentPayment, MaintenanceJob, Approval, AgentAction
from ...schemas.schemas import DashboardStats, AgentActionResponse

router = APIRouter()


@router.get("/", response_model=DashboardStats)
def get_dashboard(db: Session = Depends(get_db)):
    total_rooms = db.query(func.count(Room.id)).scalar() or 0
    occupied_rooms = db.query(func.count(Room.id)).filter(Room.status.in_(["OCCUPIED", "PARTIALLY_OCCUPIED"])).scalar() or 0
    vacant_rooms = db.query(func.count(Room.id)).filter(Room.status == "VACANT").scalar() or 0

    total_tenants = db.query(func.count(Tenant.id)).filter(Tenant.status == "ACTIVE").scalar() or 0

    total_expected_rent = db.query(func.sum(Room.rent_amount)).filter(Room.status != "VACANT").scalar() or 0
    total_pending_rent = db.query(func.sum(RentPayment.amount)).filter(RentPayment.status.in_(["PENDING", "OVERDUE"])).scalar() or 0

    open_complaints = db.query(func.count(Complaint.id)).filter(Complaint.status.in_(["OPEN", "ANALYZING", "VENDOR_SEARCH", "AWAITING_APPROVAL", "VENDOR_ASSIGNED", "IN_PROGRESS"])).scalar() or 0

    active_maintenance_jobs = db.query(func.count(MaintenanceJob.id)).filter(MaintenanceJob.status.in_(["ASSIGNED", "SCHEDULED", "IN_PROGRESS"])).scalar() or 0

    pending_approvals = db.query(func.count(Approval.id)).filter(Approval.status == "PENDING").scalar() or 0

    recent_actions = db.query(AgentAction).order_by(AgentAction.created_at.desc()).limit(10).all()

    return DashboardStats(
        total_rooms=total_rooms,
        occupied_rooms=occupied_rooms,
        vacant_rooms=vacant_rooms,
        total_tenants=total_tenants,
        total_expected_rent=float(total_expected_rent),
        total_pending_rent=float(total_pending_rent),
        open_complaints=open_complaints,
        active_maintenance_jobs=active_maintenance_jobs,
        pending_approvals=pending_approvals,
        recent_agent_actions=[AgentActionResponse.model_validate(a) for a in recent_actions],
    )
