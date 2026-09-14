from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional

from ...database import get_db
from ...models.tables import Tenant, Room
from ...schemas.schemas import TenantResponse, TenantWithRoom, RoomResponse, RoomWithTenants, TenantBrief

router = APIRouter()


class TenantCreate(BaseModel):
    room_id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., min_length=1, max_length=20)
    email: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    move_in_date: Optional[str] = None
    rent_due_day: int = 5


class TenantUpdate(BaseModel):
    room_id: Optional[int] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    rent_due_day: Optional[int] = None
    status: Optional[str] = None


@router.get("/", response_model=list[TenantWithRoom])
def list_tenants(db: Session = Depends(get_db)):
    tenants = db.query(Tenant).filter(Tenant.status == "ACTIVE").order_by(Tenant.name).all()
    result = []
    for t in tenants:
        tenant_data = TenantWithRoom.model_validate(t)
        if t.room_id:
            room = db.query(Room).filter(Room.id == t.room_id).first()
            if room:
                tenant_data.room = RoomResponse.model_validate(room)
        result.append(tenant_data)
    return result


@router.get("/{tenant_id}", response_model=TenantWithRoom)
def get_tenant(tenant_id: int, db: Session = Depends(get_db)):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    tenant_data = TenantWithRoom.model_validate(tenant)
    if tenant.room_id:
        room = db.query(Room).filter(Room.id == tenant.room_id).first()
        if room:
            tenant_data.room = RoomResponse.model_validate(room)
    return tenant_data


@router.get("/by-phone/{phone}", response_model=TenantWithRoom)
def get_tenant_by_phone(phone: str, db: Session = Depends(get_db)):
    tenant = db.query(Tenant).filter(Tenant.phone == phone, Tenant.status == "ACTIVE").first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found with this phone")
    tenant_data = TenantWithRoom.model_validate(tenant)
    if tenant.room_id:
        room = db.query(Room).filter(Room.id == tenant.room_id).first()
        if room:
            tenant_data.room = RoomResponse.model_validate(room)
    return tenant_data


@router.post("/", response_model=TenantResponse, status_code=201)
def create_tenant(data: TenantCreate, db: Session = Depends(get_db)):
    if data.room_id:
        room = db.query(Room).filter(Room.id == data.room_id).first()
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")

    tenant = Tenant(
        room_id=data.room_id,
        name=data.name,
        phone=data.phone,
        email=data.email,
        emergency_contact_name=data.emergency_contact_name,
        emergency_contact_phone=data.emergency_contact_phone,
        move_in_date=data.move_in_date,
        rent_due_day=data.rent_due_day,
        status="ACTIVE",
    )
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return TenantResponse.model_validate(tenant)


@router.put("/{tenant_id}", response_model=TenantResponse)
def update_tenant(tenant_id: int, data: TenantUpdate, db: Session = Depends(get_db)):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tenant, key, value)

    db.commit()
    db.refresh(tenant)
    return TenantResponse.model_validate(tenant)


@router.delete("/{tenant_id}")
def delete_tenant(tenant_id: int, db: Session = Depends(get_db)):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    tenant.status = "INACTIVE"
    db.commit()
    return {"status": "success", "message": f"Tenant {tenant.name} deactivated"}
