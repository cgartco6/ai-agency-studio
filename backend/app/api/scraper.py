import os
import requests
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import ScrapedLead
from pydantic import BaseModel

router = APIRouter(prefix="/scraper", tags=["Lead Generation"])

class ScraperQuery(BaseModel):
    workspace_id: int
    industry: str
    location: str = "South Africa"

@router.post("/run")
async def run_live_engine_scraper(query: ScraperQuery, db: Session = Depends(get_db)):
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")
    scraped_entries = []

    # Safe sandbox data fallback if live credentials are absent
    if not SERPAPI_KEY:
        mock_companies = ["Table Mountain Tech", "Karoo Digital", "Gauteng Media Group"]
        for idx, name in enumerate(mock_companies):
            scraped_entries.append({
                "title": name,
                "link": f"https://www.{name.lower().replace(' ', '')}.co.za",
                "snippet": "Local professional operational enterprise."
            })
    else:
        # Live Google Search execution targeting local businesses
        search_url = "https://serpapi.com"
        params = {
            "q": f"{query.industry} companies in {query.location}",
            "location": query.location,
            "hl": "en",
            "gl": "za",
            "api_key": SERPAPI_KEY
        }
        response = requests.get(search_url, params=params).json()
        scraped_entries = response.get("organic_results", [])[:5]

    saved_leads = []
    for entry in scraped_entries:
        company_name = entry.get("title", "Unknown Corporate")
        website = entry.get("link", "#")
        clean_domain = website.replace("https://www.", "").replace("http://www.", "").split("/")[0]
        
        lead_record = ScrapedLead(
            workspace_id=query.workspace_id,
            company_name=company_name,
            website=website,
            email=f"hello@{clean_domain}" if clean_domain != "#" else "info@agency.co.za",
            location=query.location,
            status="Active Target Filtered"
        )
        db.add(lead_record)
        saved_leads.append(lead_record)
        
    db.commit()

    return {
        "status": "success",
        "live_results": True if SERPAPI_KEY else False,
        "leads": [
            {"id": l.id, "company_name": l.company_name, "website": l.website, "email": l.email}
            for l in saved_leads
        ]
    }
