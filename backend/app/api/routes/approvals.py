from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from ...database import get_db
from ...models.tables import Approval
from ...schemas.schemas import ApprovalResponse, ApprovalDecision

router = APIRouter()


@router.get("/", response_model=list[ApprovalResponse])
def list_approvals(db: Session = Depends(get_db)):
    approvals = db.query(Approval).filter(Approval.status == "PENDING").order_by(Approval.created_at.desc()).all()
    return [ApprovalResponse.model_validate(a) for a in approvals]


@router.get("/{approval_id}", response_model=ApprovalResponse)
def get_approval(approval_id: int, db: Session = Depends(get_db)):
    approval = db.query(Approval).filter(Approval.id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")
    return ApprovalResponse.model_validate(approval)


@router.post("/{approval_id}/approve", response_model=ApprovalResponse)
def approve_action(approval_id: int, data: ApprovalDecision, db: Session = Depends(get_db)):
    approval = db.query(Approval).filter(Approval.id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")
    if approval.status != "PENDING":
        raise HTTPException(status_code=400, detail="Approval already decided")

    approval.status = "APPROVED"
    approval.decision_notes = data.decision_notes
    approval.approved_by = 1
    approval.decision_at = datetime.now()
    db.commit()
    db.refresh(approval)
    return ApprovalResponse.model_validate(approval)


@router.post("/{approval_id}/reject", response_model=ApprovalResponse)
def reject_action(approval_id: int, data: ApprovalDecision, db: Session = Depends(get_db)):
    approval = db.query(Approval).filter(Approval.id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")
    if approval.status != "PENDING":
        raise HTTPException(status_code=400, detail="Approval already decided")

    approval.status = "REJECTED"
    approval.decision_notes = data.decision_notes
    approval.approved_by = 1
    approval.decision_at = datetime.now()
    db.commit()
    db.refresh(approval)
    return ApprovalResponse.model_validate(approval)
