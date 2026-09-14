from strands import Agent

from ..config import get_settings
from ..tools.tenant_tools import TenantTools
from ..tools.room_tools import RoomTools
from ..tools.complaint_tools import ComplaintTools
from ..tools.vendor_tools import VendorTools
from ..tools.approval_tools import ApprovalTools
from ..tools.notification_tools import NotificationTools
from ..tools.finance_tools import FinanceTools

settings = get_settings()

OPERATIONS_SYSTEM_PROMPT = """You are the Operations Agent for HostelOps, an AI-powered hostel operations manager.

Your job is to handle maintenance complaints end-to-end. Follow these steps:

1. UNDERSTAND the complaint - what is the issue, which room, which tenant.
2. IDENTIFY the tenant using their phone number or name.
3. CLASSIFY the complaint into a category (PLUMBING, ELECTRICAL, AC, CLEANING, FURNITURE, INTERNET, APPLIANCE, SECURITY, OTHER).
4. DETERMINE priority (LOW, MEDIUM, HIGH, URGENT).
5. CREATE the complaint in the database.
6. SEARCH for vendors in the matching category.
7. COMPARE vendor options based on rating, cost, availability, and success rate.
8. RECOMMEND the best vendor with clear reasoning.
9. If cost exceeds ₹500, REQUEST OWNER APPROVAL before proceeding.
10. After approval (or if cost ≤ ₹500), CREATE the maintenance job.
11. NOTIFY the tenant about the update.
12. LOG each important action using log_agent_action.

Always use tools to interact with the database. Never make up data.
Explain your reasoning clearly when comparing vendors.
Request human approval for any action costing more than ₹500."""


def create_operations_agent(session_factory):
    """Create and return the Operations Agent with all tools."""
    tenant_tools = TenantTools(session_factory)
    room_tools = RoomTools(session_factory)
    complaint_tools = ComplaintTools(session_factory)
    vendor_tools = VendorTools(session_factory)
    approval_tools = ApprovalTools(session_factory)
    notification_tools = NotificationTools(session_factory)
    finance_tools = FinanceTools(session_factory)

    agent = Agent(
        name="operations_agent",
        description="Handles maintenance complaints, vendor management, and repair workflows",
        system_prompt=OPERATIONS_SYSTEM_PROMPT,
        tools=[
            tenant_tools.get_tenant_by_phone,
            tenant_tools.get_tenant_details,
            room_tools.get_room_details,
            room_tools.get_available_rooms,
            complaint_tools.create_complaint,
            complaint_tools.update_complaint_status,
            complaint_tools.get_complaint,
            vendor_tools.search_vendors,
            vendor_tools.get_vendor_details,
            vendor_tools.compare_vendor_options,
            vendor_tools.create_vendor_quote,
            approval_tools.create_approval_request,
            approval_tools.get_pending_approvals,
            approval_tools.create_maintenance_job,
            approval_tools.update_maintenance_job,
            notification_tools.send_notification,
            notification_tools.log_agent_action,
            finance_tools.get_pending_rent,
            finance_tools.get_rent_status,
        ],
    )
    return agent
