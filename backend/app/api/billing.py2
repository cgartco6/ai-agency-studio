from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import UserWorkspace
from pydantic import BaseModel

router = APIRouter(prefix="/billing", tags=["Billing & Payouts"])

@router.post("/webhook/payfast")
async def payfast_payment_webhook(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    payment_status = form_data.get("payment_status")
    
    # Custom variable sent during checkout initialization to track targets
    workspace_id = form_data.get("custom_int1") 
    
    if payment_status == "COMPLETE" and workspace_id:
        workspace = db.query(UserWorkspace).filter(UserWorkspace.id == int(workspace_id)).first()
        if workspace:
            # Change the target workspace model currency to reflect verified status
            workspace.currency = "ZAR_VERIFIED"
            db.commit()
            print(f"[SETTLEMENT SUCCESS]: Workspace {workspace_id} upgraded. Watermark cleared.")
            return {"status": "success", "message": "Account upgraded permanently."}
            
    return {"status": "ignored", "reason": payment_status}
