from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ...models.tables import AgentAction
from ...schemas.schemas import AgentActionResponse

router = APIRouter()


@router.get("/", response_model=list[AgentActionResponse])
def list_agent_actions(db: Session = Depends(get_db)):
    actions = db.query(AgentAction).order_by(AgentAction.created_at.desc()).limit(50).all()
    return [AgentActionResponse.model_validate(a) for a in actions]
