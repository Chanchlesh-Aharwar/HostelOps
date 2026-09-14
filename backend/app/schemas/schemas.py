from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date
from typing import Optional


# ---------- Room ----------

class RoomResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    hostel_id: int
    room_number: str
    floor: Optional[int] = None
    room_type: Optional[str] = None
    capacity: Optional[int] = None
    rent_amount: float
    security_deposit: Optional[float] = 0.0
    status: Optional[str] = "VACANT"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class RoomWithTenants(RoomResponse):
    tenants: list["TenantBrief"] = []


# ---------- Tenant ----------

class TenantBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: str
    status: Optional[str] = "ACTIVE"


class TenantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    room_id: Optional[int] = None
    name: str
    phone: str
    email: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    move_in_date: Optional[date] = None
    move_out_date: Optional[date] = None
    rent_due_day: Optional[int] = 5
    status: Optional[str] = "ACTIVE"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TenantWithRoom(TenantResponse):
    room: Optional[RoomResponse] = None


# ---------- Vendor ----------

class VendorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: str
    email: Optional[str] = None
    category: str
    rating: Optional[float] = 0.0
    average_cost: Optional[float] = 0.0
    service_area: Optional[str] = None
    availability: Optional[str] = "AVAILABLE"
    total_jobs: Optional[int] = 0
    successful_jobs: Optional[int] = 0
    status: Optional[str] = "ACTIVE"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# ---------- Complaint ----------

class ComplaintCreate(BaseModel):
    tenant_id: int
    room_id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    category: Optional[str] = "OTHER"
    priority: Optional[str] = "MEDIUM"
    source: Optional[str] = "WEB"
    image_url: Optional[str] = None


class ComplaintResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tenant_id: int
    room_id: Optional[int] = None
    title: str
    description: str
    category: Optional[str] = "OTHER"
    priority: Optional[str] = "MEDIUM"
    status: Optional[str] = "OPEN"
    source: Optional[str] = "WEB"
    image_url: Optional[str] = None
    ai_analysis: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None


class ComplaintWithDetails(ComplaintResponse):
    tenant: Optional[TenantBrief] = None
    room: Optional[RoomResponse] = None


# ---------- Rent ----------

class RentPaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tenant_id: int
    amount: float
    due_date: date
    paid_date: Optional[date] = None
    status: Optional[str] = "PENDING"
    payment_method: Optional[str] = None
    transaction_reference: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class RentPaymentWithTenant(RentPaymentResponse):
    tenant: Optional[TenantBrief] = None


class RentSummary(BaseModel):
    total_expected: float
    total_paid: float
    total_pending: float
    total_overdue: float
    paid_count: int
    pending_count: int
    overdue_count: int


# ---------- Approval ----------

class ApprovalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    action_type: str
    entity_type: str
    entity_id: int
    requested_by: Optional[str] = "AI_AGENT"
    reason: str
    status: Optional[str] = "PENDING"
    approved_by: Optional[int] = None
    decision_notes: Optional[str] = None
    created_at: Optional[datetime] = None
    decision_at: Optional[datetime] = None


class ApprovalDecision(BaseModel):
    decision_notes: Optional[str] = None


# ---------- Agent Action ----------

class AgentActionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    agent_name: str
    action_type: str
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    input_data: Optional[dict] = None
    output_data: Optional[dict] = None
    status: Optional[str] = "STARTED"
    error_message: Optional[str] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


# ---------- Dashboard ----------

class DashboardStats(BaseModel):
    total_rooms: int
    occupied_rooms: int
    vacant_rooms: int
    total_tenants: int
    total_expected_rent: float
    total_pending_rent: float
    open_complaints: int
    active_maintenance_jobs: int
    pending_approvals: int
    recent_agent_actions: list[AgentActionResponse]


# ---------- Agent Chat ----------

class AgentChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    tenant_phone: Optional[str] = None


class AgentChatResponse(BaseModel):
    response: str
    complaint_id: Optional[int] = None
    actions: list[AgentActionResponse] = []
