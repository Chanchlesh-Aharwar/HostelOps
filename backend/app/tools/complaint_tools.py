from strands import tool
from sqlalchemy.orm import Session
from datetime import datetime

from ..models.tables import Complaint, Tenant, Room


class ComplaintTools:
    """Tools for complaint-related operations."""

    def __init__(self, session_factory):
        self.session_factory = session_factory

    @tool
    def create_complaint(self, tenant_id: int, title: str, description: str, category: str = "OTHER", priority: str = "MEDIUM", room_id: int = None) -> dict:
        """Create a new maintenance complaint.

        Args:
            tenant_id: The tenant reporting the issue.
            title: Short title of the complaint.
            description: Detailed description of the issue.
            category: Category of complaint (PLUMBING, ELECTRICAL, AC, CLEANING, FURNITURE, INTERNET, APPLIANCE, SECURITY, OTHER).
            priority: Priority level (LOW, MEDIUM, HIGH, URGENT).
            room_id: Optional room ID if known.

        Returns:
            Created complaint details.
        """
        db = self.session_factory()
        try:
            tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
            if not tenant:
                return {"status": "error", "message": f"Tenant {tenant_id} not found"}

            if not room_id:
                room_id = tenant.room_id

            complaint = Complaint(
                tenant_id=tenant_id,
                room_id=room_id,
                title=title,
                description=description,
                category=category.upper(),
                priority=priority.upper(),
                status="OPEN",
                source="WEB",
            )
            db.add(complaint)
            db.commit()
            db.refresh(complaint)

            return {
                "status": "success",
                "complaint": {
                    "id": complaint.id,
                    "tenant_id": complaint.tenant_id,
                    "room_id": complaint.room_id,
                    "title": complaint.title,
                    "description": complaint.description,
                    "category": complaint.category,
                    "priority": complaint.priority,
                    "status": complaint.status,
                },
            }
        finally:
            db.close()

    @tool
    def update_complaint_status(self, complaint_id: int, status: str, ai_analysis: dict = None) -> dict:
        """Update complaint status and optionally add AI analysis.

        Args:
            complaint_id: The complaint ID.
            status: New status (OPEN, ANALYZING, VENDOR_SEARCH, AWAITING_APPROVAL, VENDOR_ASSIGNED, IN_PROGRESS, RESOLVED, CLOSED, CANCELLED).
            ai_analysis: Optional AI analysis data as JSON.

        Returns:
            Updated complaint details.
        """
        db = self.session_factory()
        try:
            complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
            if not complaint:
                return {"status": "error", "message": f"Complaint {complaint_id} not found"}

            complaint.status = status.upper()
            if ai_analysis:
                complaint.ai_analysis = ai_analysis
            if status.upper() == "RESOLVED":
                complaint.resolved_at = datetime.now()

            db.commit()
            db.refresh(complaint)

            return {
                "status": "success",
                "complaint": {
                    "id": complaint.id,
                    "status": complaint.status,
                    "ai_analysis": complaint.ai_analysis,
                },
            }
        finally:
            db.close()

    @tool
    def get_complaint(self, complaint_id: int) -> dict:
        """Get complaint details by ID.

        Args:
            complaint_id: The complaint ID.

        Returns:
            Full complaint information.
        """
        db = self.session_factory()
        try:
            complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
            if not complaint:
                return {"status": "error", "message": f"Complaint {complaint_id} not found"}

            tenant = db.query(Tenant).filter(Tenant.id == complaint.tenant_id).first()
            room = db.query(Room).filter(Room.id == complaint.room_id).first() if complaint.room_id else None

            return {
                "status": "success",
                "complaint": {
                    "id": complaint.id,
                    "tenant_id": complaint.tenant_id,
                    "tenant_name": tenant.name if tenant else None,
                    "room_id": complaint.room_id,
                    "room_number": room.room_number if room else None,
                    "title": complaint.title,
                    "description": complaint.description,
                    "category": complaint.category,
                    "priority": complaint.priority,
                    "status": complaint.status,
                    "ai_analysis": complaint.ai_analysis,
                    "created_at": str(complaint.created_at) if complaint.created_at else None,
                },
            }
        finally:
            db.close()
