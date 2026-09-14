import os
from strands import Agent
from strands.models import BedrockModel

from ..config import get_settings
from ..tools.tenant_tools import TenantTools
from ..tools.room_tools import RoomTools
from ..tools.complaint_tools import ComplaintTools
from ..tools.vendor_tools import VendorTools
from ..tools.approval_tools import ApprovalTools
from ..tools.notification_tools import NotificationTools
from ..tools.finance_tools import FinanceTools

settings = get_settings()

ORCHESTRATOR_SYSTEM_PROMPT = """You are the Orchestrator Agent for HostelOps, an AI-powered operations manager for PG and hostel owners.

Your job is to understand user requests and route them to the right specialist tools.

CAPABILITIES:
- Tenant lookup and management
- Room availability and details
- Maintenance complaints (classify, track, resolve)
- Vendor search, comparison, and assignment
- Rent tracking and payment status
- Owner approval requests
- Notifications to tenants

WORKFLOW FOR COMPLAINTS:
When someone reports a problem (e.g., "tap leak hai", "AC kaam nahi kar raha"):
1. Identify the tenant (use phone number if provided)
2. Understand and classify the issue
3. Create a complaint record
4. Search for appropriate vendors
5. Compare and recommend the best vendor
6. Request approval if cost > ₹500
7. After approval, create the maintenance job
8. Notify the tenant

Always use tools to interact with the database. Never invent data.
Log important actions for the audit trail.
Be helpful, professional, and efficient in your responses."""


def create_orchestrator(session_factory):
    """Create and return the Orchestrator Agent with all tools."""
    tenant_tools = TenantTools(session_factory)
    room_tools = RoomTools(session_factory)
    complaint_tools = ComplaintTools(session_factory)
    vendor_tools = VendorTools(session_factory)
    approval_tools = ApprovalTools(session_factory)
    notification_tools = NotificationTools(session_factory)
    finance_tools = FinanceTools(session_factory)

    model_id = settings.bedrock_model_id
    api_key = settings.bedrock_api_key or None

    if api_key:
        os.environ["AWS_BEARER_TOKEN_BEDROCK"] = api_key

    model_kwargs = {
        "model_id": model_id,
        "region_name": settings.aws_region,
    }
    if api_key:
        model_kwargs["api_key"] = api_key

    model = BedrockModel(**model_kwargs)

    agent = Agent(
        name="orchestrator",
        description="Main orchestrator that routes requests to appropriate tools",
        model=model,
        system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
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
