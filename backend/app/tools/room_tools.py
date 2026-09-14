from strands import tool
from sqlalchemy.orm import Session

from ..models.tables import Room, Tenant


class RoomTools:
    """Tools for room-related operations."""

    def __init__(self, session_factory):
        self.session_factory = session_factory

    @tool
    def get_room_details(self, room_id: int) -> dict:
        """Get room details including current tenants.

        Args:
            room_id: The room's ID.

        Returns:
            Room information with list of current tenants.
        """
        db = self.session_factory()
        try:
            room = db.query(Room).filter(Room.id == room_id).first()
            if not room:
                return {"status": "error", "message": f"Room {room_id} not found"}

            tenants = db.query(Tenant).filter(Tenant.room_id == room_id, Tenant.status == "ACTIVE").all()

            return {
                "status": "success",
                "room": {
                    "id": room.id,
                    "room_number": room.room_number,
                    "floor": room.floor,
                    "room_type": room.room_type,
                    "capacity": room.capacity,
                    "rent_amount": float(room.rent_amount),
                    "status": room.status,
                    "tenants": [
                        {"id": t.id, "name": t.name, "phone": t.phone}
                        for t in tenants
                    ],
                },
            }
        finally:
            db.close()

    @tool
    def get_available_rooms(self) -> dict:
        """Get all available rooms (vacant or partially occupied).

        Returns:
            List of available rooms with details.
        """
        db = self.session_factory()
        try:
            rooms = db.query(Room).filter(Room.status.in_(["VACANT", "PARTIALLY_OCCUPIED"])).order_by(Room.floor, Room.room_number).all()

            return {
                "status": "success",
                "rooms": [
                    {
                        "id": r.id,
                        "room_number": r.room_number,
                        "floor": r.floor,
                        "room_type": r.room_type,
                        "capacity": r.capacity,
                        "rent_amount": float(r.rent_amount),
                        "status": r.status,
                    }
                    for r in rooms
                ],
            }
        finally:
            db.close()
