from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import ScrapedLead
from pydantic import BaseModel
import random

router = APIRouter(prefix="/scraper", tags=["Lead Generation"])

class ScraperQuery(BaseModel):
    workspace_id: int
    industry: str
    location: str

@router.post("/run")
async def run_lead_scraper(query: ScraperQuery, db: Session = Depends(get_db)):
    mock_domains = ["za-creative", "randmedia", "computech", "capeagency", "joburghub"]
    new_leads_saved = []

    # Target finding pipeline execution loop
    for i in range(1, 4):
        domain = f"{random.choice(mock_domains)}{random.randint(10,99)}.co.za"
        lead_record = ScrapedLead(
            workspace_id=query.workspace_id,
            company_name=f"{query.industry.title()} Group {random.randint(1,100)}",
            website=f"https://www.{domain}",
            email=f"info@{domain}",
            location=query.location,
            status="Cold Lead Found"
        )
        db.add(lead_record)
        new_leads_saved.append(lead_record)
    
    db.commit()
    
    return {
        "status": "success",
        "scraped_count": len(new_leads_saved),
        "leads": [
            {
                "id": lead.id,
                "company_name": lead.company_name,
                "website": lead.website,
                "email": lead.email,
                "status": lead.status
            } for lead in new_leads_saved
        ]
    }
