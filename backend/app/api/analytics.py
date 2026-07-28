from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.models import Base

router = APIRouter(prefix="/analytics", tags=["Retention Analytics"])

# Database tracking entity definition
class UserClickEvent(Base):
    __tablename__ = "retention_analytics"
    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, index=True)
    ui_element_clicked = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class ClickLogPayload(BaseModel):
    workspace_id: int
    element_id: str

@router.post("/log-click")
async def register_click_event(payload: ClickLogPayload, db: Session = Depends(get_db)):
    event = UserClickEvent(
        workspace_id=payload.workspace_id,
        ui_element_clicked=payload.element_id
    )
    db.add(event)
    db.commit()
    return {"status": "telemetry_logged", "element": payload.element_id}

@router.get("/retention-summary/{workspace_id}")
async def get_retention_metrics(workspace_id: int, db: Session = Depends(get_db)):
    # Counts active system events to compute total feature interactions
    total_clicks = db.query(UserClickEvent).filter(UserClickEvent.workspace_id == workspace_id).count()
    return {
        "workspace_id": workspace_id,
        "total_active_interactions": total_clicks,
        "health_score": "High Engagement" if total_clicks > 10 else "At Risk"
    }
