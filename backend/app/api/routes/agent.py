from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...database import get_db
from ...schemas.schemas import AgentChatRequest, AgentChatResponse
from ...services.agent_service import AgentService

router = APIRouter()


@router.post("/chat", response_model=AgentChatResponse)
def chat_with_agent(data: AgentChatRequest, db: Session = Depends(get_db)):
    service = AgentService(db)
    result = service.process_message(data.message, data.tenant_phone)
    return AgentChatResponse(**result)
