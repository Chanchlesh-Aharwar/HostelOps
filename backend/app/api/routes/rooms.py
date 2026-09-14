from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional

from ...database import get_db
from ...models.tables import Room, Tenant
from ...schemas.schemas import RoomResponse, RoomWithTenants, TenantBrief

router = APIRouter()


class RoomCreate(BaseModel):
    hostel_id: int = 1
    room_number: str = Field(..., min_length=1, max_length=20)
    floor: Optional[int] = None
    room_type: str = "SINGLE"
    capacity: int = 1
    rent_amount: float = Field(..., gt=0)
    security_deposit: float = 0.0


class RoomUpdate(BaseModel):
    room_number: Optional[str] = None
    floor: Optional[int] = None
    room_type: Optional[str] = None
    capacity: Optional[int] = None
    rent_amount: Optional[float] = None
    security_deposit: Optional[float] = None
    status: Optional[str] = None


@router.get("/", response_model=list[RoomWithTenants])
def list_rooms(db: Session = Depends(get_db)):
    rooms = db.query(Room).order_by(Room.floor, Room.room_number).all()
    result = []
    for room in rooms:
        tenants = db.query(Tenant).filter(Tenant.room_id == room.id, Tenant.status == "ACTIVE").all()
        room_data = RoomWithTenants.model_validate(room)
        room_data.tenants = [TenantBrief.model_validate(t) for t in tenants]
        result.append(room_data)
    return result


@router.get("/{room_id}", response_model=RoomWithTenants)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    tenants = db.query(Tenant).filter(Tenant.room_id == room.id, Tenant.status == "ACTIVE").all()
    room_data = RoomWithTenants.model_validate(room)
    room_data.tenants = [TenantBrief.model_validate(t) for t in tenants]
    return room_data


@router.get("/available/", response_model=list[RoomResponse])
def get_available_rooms(db: Session = Depends(get_db)):
    rooms = db.query(Room).filter(Room.status.in_(["VACANT", "PARTIALLY_OCCUPIED"])).order_by(Room.floor, Room.room_number).all()
    return [RoomResponse.model_validate(r) for r in rooms]


@router.post("/", response_model=RoomResponse, status_code=201)
def create_room(data: RoomCreate, db: Session = Depends(get_db)):
    existing = db.query(Room).filter(
        Room.hostel_id == data.hostel_id,
        Room.room_number == data.room_number,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Room number already exists in this hostel")

    room = Room(
        hostel_id=data.hostel_id,
        room_number=data.room_number,
        floor=data.floor,
        room_type=data.room_type,
        capacity=data.capacity,
        rent_amount=data.rent_amount,
        security_deposit=data.security_deposit,
        status="VACANT",
    )
    db.add(room)
    db.commit()
    db.refresh(room)
    return RoomResponse.model_validate(room)


@router.put("/{room_id}", response_model=RoomResponse)
def update_room(room_id: int, data: RoomUpdate, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(room, key, value)

    db.commit()
    db.refresh(room)
    return RoomResponse.model_validate(room)


@router.delete("/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    tenants_in_room = db.query(Tenant).filter(Tenant.room_id == room_id, Tenant.status == "ACTIVE").count()
    if tenants_in_room > 0:
        raise HTTPException(status_code=400, detail="Cannot delete room with active tenants")

    db.delete(room)
    db.commit()
    return {"status": "success", "message": f"Room {room.room_number} deleted"}
