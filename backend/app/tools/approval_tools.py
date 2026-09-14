from strands import tool
from sqlalchemy.orm import Session
from datetime import datetime

from ..models.tables import Approval, MaintenanceJob, Complaint, Vendor, VendorQuote


class ApprovalTools:
    """Tools for approval and maintenance job operations."""

    def __init__(self, session_factory):
        self.session_factory = session_factory

    @tool
    def create_approval_request(self, action_type: str, entity_type: str, entity_id: int, reason: str) -> dict:
        """Create an approval request for the owner.

        Args:
            action_type: Type of action requiring approval (e.g., VENDOR_ASSIGNMENT, HIGH_COST_MAINTENANCE).
            entity_type: Type of entity (e.g., COMPLAINT, MAINTENANCE_JOB).
            entity_id: ID of the entity.
            reason: Reason why approval is needed.

        Returns:
            Created approval request details.
        """
        db = self.session_factory()
        try:
            approval = Approval(
                action_type=action_type,
                entity_type=entity_type,
                entity_id=entity_id,
                requested_by="AI_AGENT",
                reason=reason,
                status="PENDING",
            )
            db.add(approval)
            db.commit()
            db.refresh(approval)

            return {
                "status": "success",
                "approval": {
                    "id": approval.id,
                    "action_type": approval.action_type,
                    "entity_type": approval.entity_type,
                    "entity_id": approval.entity_id,
                    "reason": approval.reason,
                    "status": approval.status,
                },
            }
        finally:
            db.close()

    @tool
    def get_pending_approvals(self) -> dict:
        """Get all pending approval requests.

        Returns:
            List of pending approvals.
        """
        db = self.session_factory()
        try:
            approvals = db.query(Approval).filter(
                Approval.status == "PENDING"
            ).order_by(Approval.created_at.desc()).all()

            return {
                "status": "success",
                "approvals": [
                    {
                        "id": a.id,
                        "action_type": a.action_type,
                        "entity_type": a.entity_type,
                        "entity_id": a.entity_id,
                        "requested_by": a.requested_by,
                        "reason": a.reason,
                        "status": a.status,
                        "created_at": str(a.created_at) if a.created_at else None,
                    }
                    for a in approvals
                ],
                "total": len(approvals),
            }
        finally:
            db.close()

    @tool
    def create_maintenance_job(self, complaint_id: int, vendor_id: int, agreed_amount: float, quote_id: int = None) -> dict:
        """Create a maintenance job after approval.

        Args:
            complaint_id: The complaint ID.
            vendor_id: The assigned vendor ID.
            agreed_amount: Agreed cost for the job.
            quote_id: Optional quote ID.

        Returns:
            Created job details.
        """
        db = self.session_factory()
        try:
            job = MaintenanceJob(
                complaint_id=complaint_id,
                vendor_id=vendor_id,
                quote_id=quote_id,
                agreed_amount=agreed_amount,
                status="ASSIGNED",
            )
            db.add(job)

            db.query(Complaint).filter(Complaint.id == complaint_id).update({"status": "VENDOR_ASSIGNED"})
            db.query(Vendor).filter(Vendor.id == vendor_id).update({"total_jobs": Vendor.total_jobs + 1})

            db.commit()
            db.refresh(job)

            vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()

            return {
                "status": "success",
                "job": {
                    "id": job.id,
                    "complaint_id": job.complaint_id,
                    "vendor_id": job.vendor_id,
                    "vendor_name": vendor.name if vendor else "Unknown",
                    "agreed_amount": float(job.agreed_amount),
                    "status": job.status,
                    "assigned_at": str(job.assigned_at) if job.assigned_at else None,
                },
            }
        finally:
            db.close()

    @tool
    def update_maintenance_job(self, job_id: int, status: str, completion_notes: str = None) -> dict:
        """Update maintenance job status.

        Args:
            job_id: The job ID.
            status: New status (ASSIGNED, SCHEDULED, IN_PROGRESS, COMPLETED, CANCELLED).
            completion_notes: Optional notes on completion.

        Returns:
            Updated job details.
        """
        db = self.session_factory()
        try:
            job = db.query(MaintenanceJob).filter(MaintenanceJob.id == job_id).first()
            if not job:
                return {"status": "error", "message": f"Job {job_id} not found"}

            job.status = status.upper()
            if completion_notes:
                job.completion_notes = completion_notes
            if status.upper() == "COMPLETED":
                job.completed_at = datetime.now()
                db.query(Complaint).filter(Complaint.id == job.complaint_id).update({"status": "RESOLVED"})
            elif status.upper() == "IN_PROGRESS":
                job.started_at = datetime.now()

            db.commit()
            db.refresh(job)

            return {
                "status": "success",
                "job": {
                    "id": job.id,
                    "status": job.status,
                    "completion_notes": job.completion_notes,
                },
            }
        finally:
            db.close()
