from strands import tool
from sqlalchemy.orm import Session

from ..models.tables import Tenant, Room


class TenantTools:
    """Tools for tenant-related operations."""

    def __init__(self, session_factory):
        self.session_factory = session_factory

    @tool
    def get_tenant_by_phone(self, phone: str) -> dict:
        """Find a tenant by their phone number.

        Args:
            phone: The tenant's phone number.

        Returns:
            Tenant information including name, room, and status.
        """
        db = self.session_factory()
        try:
            tenant = db.query(Tenant).filter(Tenant.phone == phone, Tenant.status == "ACTIVE").first()
            if not tenant:
                return {"status": "error", "message": f"No active tenant found with phone {phone}"}

            room = db.query(Room).filter(Room.id == tenant.room_id).first() if tenant.room_id else None

            return {
                "status": "success",
                "tenant": {
                    "id": tenant.id,
                    "name": tenant.name,
                    "phone": tenant.phone,
                    "email": tenant.email,
                    "room_id": tenant.room_id,
                    "room_number": room.room_number if room else None,
                    "floor": room.floor if room else None,
                    "rent_amount": float(room.rent_amount) if room else None,
                    "status": tenant.status,
                },
            }
        finally:
            db.close()

    @tool
    def get_tenant_details(self, tenant_id: int) -> dict:
        """Get full details of a tenant by ID.

        Args:
            tenant_id: The tenant's ID.

        Returns:
            Complete tenant information.
        """
        db = self.session_factory()
        try:
            tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
            if not tenant:
                return {"status": "error", "message": f"Tenant {tenant_id} not found"}

            room = db.query(Room).filter(Room.id == tenant.room_id).first() if tenant.room_id else None

            return {
                "status": "success",
                "tenant": {
                    "id": tenant.id,
                    "name": tenant.name,
                    "phone": tenant.phone,
                    "email": tenant.email,
                    "emergency_contact_name": tenant.emergency_contact_name,
                    "emergency_contact_phone": tenant.emergency_contact_phone,
                    "room_id": tenant.room_id,
                    "room_number": room.room_number if room else None,
                    "floor": room.floor if room else None,
                    "rent_amount": float(room.rent_amount) if room else None,
                    "move_in_date": str(tenant.move_in_date) if tenant.move_in_date else None,
                    "status": tenant.status,
                },
            }
        finally:
            db.close()
