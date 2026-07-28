from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import UserWorkspace, ScrapedLead, GeneratedAsset
from app.api.analytics import UserClickEvent

router = APIRouter(prefix="/admin", tags=["Global Admin Matrix"])

@router.get("/dashboard-metrics")
async def get_global_admin_metrics(db: Session = Depends(get_db)):
    try:
        total_workspaces = db.query(UserWorkspace).count()
        verified_workspaces = db.query(UserWorkspace).filter(UserWorkspace.currency == "ZAR_VERIFIED").count()
        trial_workspaces = total_workspaces - verified_workspaces
        
        total_leads_scraped = db.query(ScrapedLead).count()
        total_assets_compiled = db.query(GeneratedAsset).count()
        total_telemetry_clicks = db.query(UserClickEvent).count()
        
        # Calculate gross revenue safely assuming standard R450 base pricing index
        gross_revenue_zar = verified_workspaces * 450.00
        
        return {
            "status": "success",
            "kpis": {
                "total_registered_studios": total_workspaces,
                "active_premium_studios": verified_workspaces,
                "active_trial_studios": trial_workspaces,
                "total_leads_captured": total_leads_scraped,
                "total_packages_bundled": total_assets_compiled,
                "global_telemetry_events": total_telemetry_clicks,
                "estimated_gross_revenue": f"R{gross_revenue_zar:,.2f} ZAR"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Admin cluster matrix failed: {str(e)}")
