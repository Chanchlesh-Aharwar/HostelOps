"""Tests for agent tools."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.tools.tenant_tools import TenantTools
from app.tools.room_tools import RoomTools
from app.tools.complaint_tools import ComplaintTools
from app.tools.vendor_tools import VendorTools
from app.tools.finance_tools import FinanceTools
from app.tools.approval_tools import ApprovalTools
from app.tools.notification_tools import NotificationTools


@pytest.fixture(scope="module")
def db_session():
    engine = create_engine("sqlite:///test.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture(scope="module")
def session_factory():
    engine = create_engine("sqlite:///test.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session


def test_tenant_tools_init(session_factory):
    tools = TenantTools(session_factory)
    assert tools is not None


def test_room_tools_init(session_factory):
    tools = RoomTools(session_factory)
    assert tools is not None


def test_complaint_tools_init(session_factory):
    tools = ComplaintTools(session_factory)
    assert tools is not None


def test_vendor_tools_init(session_factory):
    tools = VendorTools(session_factory)
    assert tools is not None


def test_finance_tools_init(session_factory):
    tools = FinanceTools(session_factory)
    assert tools is not None


def test_approval_tools_init(session_factory):
    tools = ApprovalTools(session_factory)
    assert tools is not None


def test_notification_tools_init(session_factory):
    tools = NotificationTools(session_factory)
    assert tools is not None
