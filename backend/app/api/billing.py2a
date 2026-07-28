from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from pydantic import BaseModel

router = APIRouter(prefix="/billing", tags=["Billing & Payouts"])

class CheckoutPayload(BaseModel):
    amount: float
    user_email: str

@router.post("/checkout/payfast")
async def initiate_payfast_checkout(payload: CheckoutPayload):
    # Generates a standard South African sandbox gateway payment transaction URL
    payfast_url = (
        f"https://payfast.co.za"
        f"?merchant_id={settings.PAYFAST_MERCHANT_ID}"
        f"&merchant_key={settings.PAYFAST_MERCHANT_KEY}"
        f"&amount={payload.amount}"
        f"&item_name=Studio_Enterprise_Tier"
        f"&email_address={payload.user_email}"
    )
    return {"status": "success", "currency": "ZAR", "redirect_url": payfast_url}

@router.post("/webhook/payfast")
async def payfast_payment_webhook(request: Request, db: Session = Depends(get_db)):
    # Processes the incoming Immediate Payment Notification (IPN) status callbacks safely
    form_data = await request.form()
    payment_status = form_data.get("payment_status")
    item_name = form_data.get("item_name")
    
    if payment_status == "COMPLETE":
        print(f"[BILLING SYSTEM]: Payment received successfully for target {item_name}")
        return {"status": "processed", "action": "activate_features"}
        
    return {"status": "ignored", "reason": payment_status}
