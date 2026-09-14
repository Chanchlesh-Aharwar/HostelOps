from sqlalchemy import Table, Column, BigInteger, String, Text, Integer, Numeric, Enum, JSON, DateTime, Date, SmallInteger, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date
from typing import Optional

from ..database import Base


# ---------- Users ----------

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(10), default="OWNER")
    is_active: Mapped[bool] = mapped_column(SmallInteger, default=1)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


# ---------- Hostels ----------

class Hostel(Base):
    __tablename__ = "hostels"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(150))
    address: Mapped[str] = mapped_column(Text)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    pincode: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    total_rooms: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    contact_phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


# ---------- Rooms ----------

class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    hostel_id: Mapped[int] = mapped_column(BigInteger)
    room_number: Mapped[str] = mapped_column(String(20))
    floor: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    room_type: Mapped[Optional[str]] = mapped_column(String(20), default="SINGLE")
    capacity: Mapped[Optional[int]] = mapped_column(Integer, default=1)
    rent_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    security_deposit: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), default=0.00)
    status: Mapped[Optional[str]] = mapped_column(String(20), default="VACANT")
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


# ---------- Tenants ----------

class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    room_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    emergency_contact_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    emergency_contact_phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    move_in_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    move_out_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    rent_due_day: Mapped[Optional[int]] = mapped_column(Integer, default=5)
    status: Mapped[Optional[str]] = mapped_column(String(20), default="ACTIVE")
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


# ---------- Rent Payments ----------

class RentPayment(Base):
    __tablename__ = "rent_payments"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    tenant_id: Mapped[int] = mapped_column(BigInteger)
    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    due_date: Mapped[date] = mapped_column(Date)
    paid_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String(20), default="PENDING")
    payment_method: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    transaction_reference: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


# ---------- Complaints ----------

class Complaint(Base):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    tenant_id: Mapped[int] = mapped_column(BigInteger)
    room_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[Optional[str]] = mapped_column(String(20), default="OTHER")
    priority: Mapped[Optional[str]] = mapped_column(String(10), default="MEDIUM")
    status: Mapped[Optional[str]] = mapped_column(String(20), default="OPEN")
    source: Mapped[Optional[str]] = mapped_column(String(10), default="WEB")
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    ai_analysis: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


# ---------- Vendors ----------

class Vendor(Base):
    __tablename__ = "vendors"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150))
    phone: Mapped[str] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    category: Mapped[str] = mapped_column(String(20))
    rating: Mapped[Optional[float]] = mapped_column(Numeric(2, 1), default=0.0)
    average_cost: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), default=0.00)
    service_area: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    availability: Mapped[Optional[str]] = mapped_column(String(20), default="AVAILABLE")
    total_jobs: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    successful_jobs: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    status: Mapped[Optional[str]] = mapped_column(String(20), default="ACTIVE")
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


# ---------- Vendor Quotes ----------

class VendorQuote(Base):
    __tablename__ = "vendor_quotes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    complaint_id: Mapped[int] = mapped_column(BigInteger)
    vendor_id: Mapped[int] = mapped_column(BigInteger)
    quoted_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    estimated_time_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    available_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String(20), default="RECEIVED")
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


# ---------- Maintenance Jobs ----------

class MaintenanceJob(Base):
    __tablename__ = "maintenance_jobs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    complaint_id: Mapped[int] = mapped_column(BigInteger)
    vendor_id: Mapped[int] = mapped_column(BigInteger)
    quote_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    assigned_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    agreed_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    status: Mapped[Optional[str]] = mapped_column(String(20), default="ASSIGNED")
    completion_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


# ---------- Messages ----------

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    tenant_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    direction: Mapped[str] = mapped_column(String(10))
    channel: Mapped[str] = mapped_column(String(10))
    message_type: Mapped[Optional[str]] = mapped_column(String(10), default="TEXT")
    message_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    media_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    external_message_id: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    processed: Mapped[Optional[bool]] = mapped_column(SmallInteger, default=0)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())


# ---------- Approvals ----------

class Approval(Base):
    __tablename__ = "approvals"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    action_type: Mapped[str] = mapped_column(String(100))
    entity_type: Mapped[str] = mapped_column(String(50))
    entity_id: Mapped[int] = mapped_column(BigInteger)
    requested_by: Mapped[Optional[str]] = mapped_column(String(100), default="AI_AGENT")
    reason: Mapped[str] = mapped_column(Text)
    status: Mapped[Optional[str]] = mapped_column(String(20), default="PENDING")
    approved_by: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    decision_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())
    decision_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


# ---------- Attachments ----------

class Attachment(Base):
    __tablename__ = "attachments"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    complaint_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    file_name: Mapped[str] = mapped_column(String(255))
    file_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    file_size: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    file_url: Mapped[str] = mapped_column(String(500))
    ai_analysis: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())


# ---------- Agent Actions ----------

class AgentAction(Base):
    __tablename__ = "agent_actions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    agent_name: Mapped[str] = mapped_column(String(100))
    action_type: Mapped[str] = mapped_column(String(100))
    entity_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    entity_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    input_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    output_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String(20), default="STARTED")
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
