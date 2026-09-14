"""Tests for API routes."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_dashboard():
    response = client.get("/api/dashboard/")
    assert response.status_code == 200
    data = response.json()
    assert "total_rooms" in data
    assert "total_tenants" in data


def test_rooms():
    response = client.get("/api/rooms/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_tenants():
    response = client.get("/api/tenants/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_vendors():
    response = client.get("/api/vendors/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_complaints():
    response = client.get("/api/complaints/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_rent_summary():
    response = client.get("/api/rent/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_expected" in data


def test_approvals():
    response = client.get("/api/approvals/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_agent_actions():
    response = client.get("/api/agent/actions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_complaint():
    response = client.post("/api/complaints/", json={
        "tenant_id": 1,
        "title": "Test complaint",
        "description": "Test description for plumbing issue",
        "category": "PLUMBING",
        "priority": "MEDIUM",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test complaint"
    assert data["category"] == "PLUMBING"


def test_agent_chat():
    response = client.post("/api/agent/chat", json={
        "message": "Room 101 ka tap leak ho raha hai",
        "tenant_phone": "9800000001",
    })
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert len(data["response"]) > 0


def test_whatsapp_webhook():
    response = client.post("/api/whatsapp/webhook", json={
        "phone": "9800000001",
        "text": "Bathroom tap leak ho raha hai",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["processed", "received"]
