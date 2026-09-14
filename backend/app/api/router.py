from fastapi import APIRouter

from .routes import dashboard, rooms, tenants, vendors, complaints, rent, approvals, agent_actions, agent, whatsapp, rent_auto

api_router = APIRouter(prefix="/api")

api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(rooms.router, prefix="/rooms", tags=["Rooms"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["Tenants"])
api_router.include_router(vendors.router, prefix="/vendors", tags=["Vendors"])
api_router.include_router(complaints.router, prefix="/complaints", tags=["Complaints"])
api_router.include_router(rent.router, prefix="/rent", tags=["Rent"])
api_router.include_router(rent_auto.router, prefix="/rent/auto", tags=["Rent Automation"])
api_router.include_router(approvals.router, prefix="/approvals", tags=["Approvals"])
api_router.include_router(agent_actions.router, prefix="/agent/actions", tags=["Agent Actions"])
api_router.include_router(agent.router, prefix="/agent", tags=["Agent"])
api_router.include_router(whatsapp.router, prefix="/whatsapp", tags=["WhatsApp"])
