from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from ...database import get_db
from ...models.tables import Complaint, Tenant, Room, Attachment
from ...schemas.schemas import ComplaintCreate, ComplaintResponse, ComplaintWithDetails, TenantBrief, RoomResponse
from ...services.image_service import analyze_complaint_image, save_upload, ALLOWED_TYPES, MAX_SIZE_MB

router = APIRouter()


@router.get("/", response_model=list[ComplaintWithDetails])
def list_complaints(db: Session = Depends(get_db)):
    complaints = db.query(Complaint).order_by(Complaint.created_at.desc()).all()
    result = []
    for c in complaints:
        complaint_data = ComplaintWithDetails.model_validate(c)
        if c.tenant_id:
            tenant = db.query(Tenant).filter(Tenant.id == c.tenant_id).first()
            if tenant:
                complaint_data.tenant = TenantBrief.model_validate(tenant)
        if c.room_id:
            room = db.query(Room).filter(Room.id == c.room_id).first()
            if room:
                complaint_data.room = RoomResponse.model_validate(room)
        result.append(complaint_data)
    return result


@router.get("/{complaint_id}", response_model=ComplaintWithDetails)
def get_complaint(complaint_id: int, db: Session = Depends(get_db)):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    complaint_data = ComplaintWithDetails.model_validate(complaint)
    if complaint.tenant_id:
        tenant = db.query(Tenant).filter(Tenant.id == complaint.tenant_id).first()
        if tenant:
            complaint_data.tenant = TenantBrief.model_validate(tenant)
    if complaint.room_id:
        room = db.query(Room).filter(Room.id == complaint.room_id).first()
        if room:
            complaint_data.room = RoomResponse.model_validate(room)
    return complaint_data


@router.post("/", response_model=ComplaintResponse, status_code=201)
def create_complaint(data: ComplaintCreate, db: Session = Depends(get_db)):
    tenant = db.query(Tenant).filter(Tenant.id == data.tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    complaint = Complaint(
        tenant_id=data.tenant_id,
        room_id=data.room_id or tenant.room_id,
        title=data.title,
        description=data.description,
        category=data.category,
        priority=data.priority,
        source=data.source,
        image_url=data.image_url,
        status="OPEN",
    )
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    return ComplaintResponse.model_validate(complaint)


@router.post("/{complaint_id}/upload-image")
async def upload_complaint_image(
    complaint_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Upload an image for a complaint and analyze it with AI vision."""
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail=f"File type {file.content_type} not allowed")

    content = await file.read()
    if len(content) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File too large (max {MAX_SIZE_MB}MB)")

    file_path = save_upload(content, file.filename, file.content_type)

    attachment = Attachment(
        complaint_id=complaint_id,
        file_name=file.filename,
        file_type=file.content_type,
        file_size=len(content),
        file_url=file_path,
    )
    db.add(attachment)

    analysis = analyze_complaint_image(file_path, complaint.description)
    attachment.ai_analysis = analysis

    complaint.image_url = file_path
    if analysis.get("category"):
        complaint.category = analysis["category"]
    complaint.ai_analysis = analysis

    db.commit()
    db.refresh(complaint)

    return {
        "status": "success",
        "complaint_id": complaint_id,
        "file_url": file_path,
        "analysis": analysis,
    }
