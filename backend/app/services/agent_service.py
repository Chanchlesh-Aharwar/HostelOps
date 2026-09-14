"""
Agent Service - Strands Agent integration.
Connects the API layer to the AI agent system.
"""

import logging
import os
from sqlalchemy.orm import Session, sessionmaker

from ..database import SessionLocal
from ..config import get_settings
from ..agents.orchestrator import create_orchestrator

logger = logging.getLogger(__name__)
settings = get_settings()

# Module-level agent instance (singleton pattern)
_orchestrator = None


def _get_orchestrator():
    """Get or create the orchestrator agent singleton."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = create_orchestrator(SessionLocal)
        logger.info("Orchestrator agent initialized")
    return _orchestrator


class AgentService:
    def __init__(self, db: Session):
        self.db = db

    def process_message(self, message: str, tenant_phone: str = None) -> dict:
        """
        Process a message through the AI agent.

        The agent will:
        1. Understand the request
        2. Use tools to interact with the database
        3. Make decisions and take actions
        4. Return a response
        """
        try:
            # Check if AWS credentials are configured
            if not settings.aws_access_key_id or not settings.aws_secret_access_key:
                logger.warning("AWS credentials not configured. Using mock response.")
                return self._mock_process(message, tenant_phone)

            orchestrator = _get_orchestrator()

            # Build the prompt with context
            prompt = message
            if tenant_phone:
                prompt = f"Tenant phone: {tenant_phone}\nMessage: {message}"

            # Invoke the agent
            result = orchestrator(prompt)

            # Extract response
            response_text = result.output if hasattr(result, 'output') else str(result)

            return {
                "response": response_text,
                "complaint_id": None,
                "actions": [],
            }

        except Exception as e:
            logger.error(f"Agent processing error: {e}, falling back to mock")
            return self._mock_process(message, tenant_phone)

    def _mock_process(self, message: str, tenant_phone: str = None) -> dict:
        """
        Mock processing when AWS credentials are not available.
        Demonstrates the workflow without actual LLM calls.
        """
        from ..models.tables import Tenant, Room, Complaint, Vendor, VendorQuote, Approval, AgentAction, MaintenanceJob
        from datetime import datetime

        message_lower = message.lower()
        actions_log = []

        # Step 1: Identify tenant
        tenant = None
        if tenant_phone:
            tenant = self.db.query(Tenant).filter(Tenant.phone == tenant_phone, Tenant.status == "ACTIVE").first()

        if not tenant and ("tap" in message_lower or "leak" in message_lower or "complaint" in message_lower):
            tenant = self.db.query(Tenant).filter(Tenant.status == "ACTIVE").first()

        if not tenant:
            return {
                "response": "I couldn't identify a tenant. Please provide a phone number or tenant name.",
                "complaint_id": None,
                "actions": [],
            }

        # Get room info
        room = self.db.query(Room).filter(Room.id == tenant.room_id).first() if tenant.room_id else None

        # Step 2: Classify complaint
        category = "OTHER"
        if "tap" in message_lower or "leak" in message_lower or "plumb" in message_lower or "bathroom" in message_lower:
            category = "PLUMBING"
        elif "electric" in message_lower or "light" in message_lower or "fan" in message_lower:
            category = "ELECTRICAL"
        elif "ac" in message_lower or "cool" in message_lower or "air" in message_lower:
            category = "AC"
        elif "clean" in message_lower:
            category = "CLEANING"
        elif "furnitur" in message_lower or "bed" in message_lower or "table" in message_lower:
            category = "FURNITURE"
        elif "internet" in message_lower or "wifi" in message_lower:
            category = "INTERNET"

        # Step 3: Determine priority
        priority = "MEDIUM"
        if "urgent" in message_lower or "emergency" in message_lower:
            priority = "URGENT"
        elif "leak" in message_lower or "electrical" in message_lower:
            priority = "HIGH"

        # Log action
        action1 = AgentAction(
            agent_name="orchestrator",
            action_type="CLASSIFY_COMPLAINT",
            entity_type="COMPLAINT",
            input_data={"message": message, "tenant_id": tenant.id},
            output_data={"category": category, "priority": priority},
            status="SUCCESS",
            completed_at=datetime.now(),
        )
        self.db.add(action1)

        # Step 4: Create complaint
        complaint = Complaint(
            tenant_id=tenant.id,
            room_id=tenant.room_id,
            title=message[:200],
            description=message,
            category=category,
            priority=priority,
            status="OPEN",
            source="WEB",
            ai_analysis={
                "category": category,
                "priority": priority,
                "confidence": 0.85,
                "agent_reasoning": f"Classified as {category} based on keywords in the message.",
            },
        )
        self.db.add(complaint)
        self.db.flush()

        action2 = AgentAction(
            agent_name="orchestrator",
            action_type="CREATE_COMPLAINT",
            entity_type="COMPLAINT",
            entity_id=complaint.id,
            input_data={"tenant_id": tenant.id, "category": category},
            output_data={"complaint_id": complaint.id, "status": "OPEN"},
            status="SUCCESS",
            completed_at=datetime.now(),
        )
        self.db.add(action2)

        # Step 5: Search vendors
        vendors = self.db.query(Vendor).filter(
            Vendor.category == category,
            Vendor.status == "ACTIVE",
            Vendor.availability != "UNAVAILABLE",
        ).order_by(Vendor.rating.desc()).all()

        action3 = AgentAction(
            agent_name="orchestrator",
            action_type="SEARCH_VENDORS",
            entity_type="VENDOR",
            input_data={"category": category},
            output_data={"vendors_found": len(vendors), "vendor_ids": [v.id for v in vendors]},
            status="SUCCESS",
            completed_at=datetime.now(),
        )
        self.db.add(action3)

        # Step 6: Compare vendors
        vendor_comparison = []
        for v in vendors[:3]:
            vendor_comparison.append({
                "id": v.id,
                "name": v.name,
                "rating": float(v.rating),
                "average_cost": float(v.average_cost),
                "availability": v.availability,
                "success_rate": round(v.successful_jobs / v.total_jobs * 100, 1) if v.total_jobs > 0 else 0,
            })

        # Create quotes for top vendors
        for v in vendors[:3]:
            quote = VendorQuote(
                complaint_id=complaint.id,
                vendor_id=v.id,
                quoted_amount=v.average_cost,
                estimated_time_minutes=60,
                status="RECEIVED",
            )
            self.db.add(quote)

        action4 = AgentAction(
            agent_name="orchestrator",
            action_type="COMPARE_VENDORS",
            entity_type="VENDOR",
            input_data={"vendor_ids": [v.id for v in vendors[:3]]},
            output_data={"comparison": vendor_comparison},
            status="SUCCESS",
            completed_at=datetime.now(),
        )
        self.db.add(action4)

        # Step 7: Update complaint status
        complaint.status = "VENDOR_SEARCH"

        # Step 8: Recommend best vendor
        best_vendor = vendors[0] if vendors else None
        recommendation_reason = ""
        if best_vendor:
            recommendation_reason = (
                f"Recommended {best_vendor.name} (Rating: {best_vendor.rating}/5, "
                f"Average Cost: ₹{best_vendor.average_cost}, "
                f"Availability: {best_vendor.availability}). "
                f"This vendor has the highest rating and good availability."
            )

        # Step 9: Check if approval needed
        estimated_cost = float(best_vendor.average_cost) if best_vendor else 0
        needs_approval = estimated_cost > 500

        if needs_approval and best_vendor:
            complaint.status = "AWAITING_APPROVAL"
            approval = Approval(
                action_type="VENDOR_ASSIGNMENT",
                entity_type="COMPLAINT",
                entity_id=complaint.id,
                requested_by="AI_AGENT",
                reason=f"Vendor assignment for {category} complaint in Room {room.room_number if room else 'Unknown'}. "
                       f"Recommended: {best_vendor.name} (₹{best_vendor.average_cost}). "
                       f"Reason: Highest rating ({best_vendor.rating}/5), {best_vendor.availability}.",
                status="PENDING",
            )
            self.db.add(approval)

            action5 = AgentAction(
                agent_name="orchestrator",
                action_type="REQUEST_APPROVAL",
                entity_type="APPROVAL",
                entity_id=approval.id,
                input_data={"vendor_id": best_vendor.id, "estimated_cost": estimated_cost},
                output_data={"approval_id": approval.id, "reason": recommendation_reason},
                status="WAITING_APPROVAL",
                completed_at=datetime.now(),
            )
            self.db.add(action5)

        self.db.commit()

        # Step 10: Build response
        response_parts = [
            f"**Complaint Registered** (ID: #{complaint.id})",
            f"**Tenant**: {tenant.name} (Room {room.room_number if room else 'N/A'})",
            f"**Category**: {category} | **Priority**: {priority}",
            f"**Status**: {complaint.status}",
            "",
        ]

        if vendor_comparison:
            response_parts.append("**Vendor Comparison:**")
            for vc in vendor_comparison:
                response_parts.append(
                    f"  - {vc['name']}: Rating {vc['rating']}/5, ₹{vc['average_cost']}, {vc['availability']}"
                )
            response_parts.append("")

        if recommendation_reason:
            response_parts.append(f"**AI Recommendation:** {recommendation_reason}")

        if needs_approval:
            response_parts.append("")
            response_parts.append("**Owner approval required** (cost > ₹500). Approval request sent to dashboard.")
        else:
            # Auto-assign if cost ≤ ₹500
            if best_vendor:
                job = MaintenanceJob(
                    complaint_id=complaint.id,
                    vendor_id=best_vendor.id,
                    agreed_amount=best_vendor.average_cost,
                    status="ASSIGNED",
                )
                self.db.add(job)
                complaint.status = "VENDOR_ASSIGNED"
                self.db.commit()
                response_parts.append("")
                response_parts.append(f"**Auto-approved** (cost ≤ ₹500). Vendor {best_vendor.name} assigned.")

        response_text = "\n".join(response_parts)

        return {
            "response": response_text,
            "complaint_id": complaint.id,
            "actions": [],
        }
