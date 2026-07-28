import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI

router = APIRouter(prefix="/ai", tags=["AI Copy Generation"])

class AICopyRequest(BaseModel):
    brand_name: str
    industry: str
    niche_focus: str

@router.post("/generate-copy")
async def generate_landing_copy(payload: AICopyRequest):
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    if not OPENAI_API_KEY:
        # High-utility fallback marketing text if API token is missing
        return {
            "status": "fallback",
            "headline": f"Next-Gen Digital Solutions for {payload.industry}",
            "subheadline": f"We elevate your business with elite {payload.niche_focus} infrastructure built for conversion.",
            "cta_text": "Secure Your Transformation"
        }
        
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        system_prompt = "You are an elite conversion copywriter for a top-tier digital branding agency."
        user_prompt = (
            f"Write copy for an agency named '{payload.brand_name}' specializing in {payload.industry}. "
            f"Focus on {payload.niche_focus}. Return EXACTLY three lines separated by pipes (|) in this format: "
            f"Headline | Subheadline | Call to Action text. Keep it short, sharp, and highly professional."
        )
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        raw_text = response.choices[0].message.content.strip()
        parts = [p.strip() for p in raw_text.split("|")]
        
        if len(parts) >= 3:
            return {"status": "success", "headline": parts[0], "subheadline": parts[1], "cta_text": parts[2]}
        else:
            raise ValueError("Unexpected response structure layout from model runtime.")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI model pipeline error: {str(e)}")
