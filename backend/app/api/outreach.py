import os
import requests
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from twilio.rest import Client

router = APIRouter(prefix="/outreach", tags=["SMS Communications"])

class SMSLeadItem(BaseModel):
    company_name: str
    phone_number: str # Ensure collected targets match standard E.164 formatting (+27...)

class SMSBlastPayload(BaseModel):
    workspace_id: int
    targets: List[SMSLeadItem]
    sender_brand: str

@router.post("/blast-sms/twilio")
async def deploy_twilio_sms(payload: SMSBlastPayload):
    TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
    dispatched = 0

    if not TWILIO_SID or not TWILIO_AUTH:
        return {"status": "mock_mode", "message": "Twilio parameters missing. SMS delivery skipped.", "count": len(payload.targets)}

    client = Client(TWILIO_SID, TWILIO_AUTH)
    for target in payload.targets:
        message_body = f"Hello {target.company_name}. {payload.sender_brand} has generated a new digital conversion profile for you. Let's grow your digital presence."
        client.messages.create(
            body=message_body,
            from_=TWILIO_NUMBER,
            to=target.phone_number
        )
        dispatched += 1

    return {"status": "success", "gateway": "Twilio International", "dispatched_count": dispatched}

@router.post("/blast-sms/bulksms")
async def deploy_bulksms_za(payload: SMSBlastPayload):
    BULKSMS_TOKEN_ID = os.getenv("BULKSMS_TOKEN_ID")
    BULKSMS_TOKEN_SECRET = os.getenv("BULKSMS_TOKEN_SECRET")
    dispatched = 0

    if not BULKSMS_TOKEN_ID or not BULKSMS_TOKEN_SECRET:
        return {"status": "mock_mode", "message": "BulkSMS South Africa keys missing.", "count": len(payload.targets)}

    # Direct South African routing optimization payload map
    for target in payload.targets:
        sms_data = [{
            "to": target.phone_number,
            "body": f"Hi {target.company_name}. Tailored creative assets are ready from {payload.sender_brand}."
        }]
        requests.post(
            "https://bulksms.com",
            auth=(BULKSMS_TOKEN_ID, BULKSMS_TOKEN_SECRET),
            json=sms_data
        )
        dispatched += 1

    return {"status": "success", "gateway": "BulkSMS South Africa", "dispatched_count": dispatched}
