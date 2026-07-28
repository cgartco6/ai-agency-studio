import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/currency", tags=["Global Currency Localization"])

class ConversionRequest(BaseModel):
    base_amount_zar: float = 450.00
    target_iso_code: str # e.g., USD, EUR, GBP

@router.post("/convert-price")
async def calculate_localized_price(payload: ConversionRequest):
    target_currency = payload.target_iso_code.upper()
    
    # Fast access fallback map if external exchange services are unreachable
    fallback_rates = {"USD": 0.054, "EUR": 0.050, "GBP": 0.042}
    
    try:
        # Request live exchange metrics from a public exchange rate interface
        api_url = f"https://er-api.com"
        response = requests.get(api_url, timeout=5)
        
        if response.status_code == 200:
            rates = response.json().get("rates", {})
            conversion_rate = rates.get(target_currency)
            
            if conversion_rate:
                localized_sum = payload.base_amount_zar * conversion_rate
                return {
                    "base_amount": f"R{payload.base_amount_zar:.2f} ZAR",
                    "converted_amount": f"{localized_sum:.2f} {target_currency}",
                    "live_rate_applied": conversion_rate,
                    "data_source": "Live Exchange Network"
                }
                
        raise ValueError("Target ticker ISO mismatch or network connection timeout.")
        
    except Exception:
        # Fall back gracefully to preset metrics to keep invoicing channels online
        rate = fallback_rates.get(target_currency, 1.0)
        localized_sum = payload.base_amount_zar * rate
        return {
            "base_amount": f"R{payload.base_amount_zar:.2f} ZAR",
            "converted_amount": f"{localized_sum:.2f} {target_currency}",
            "live_rate_applied": rate,
            "data_source": "Internal Fallback Core Matrix"
        }
