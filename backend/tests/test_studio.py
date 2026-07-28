import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_system_root_status():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "Online"
    assert response.json()["default_currency"] == "ZAR"

def test_user_workspace_registration():
    payload = {
        "email": "test_agency@studio.co.za",
        "password": "securepassword123",
        "company_name": "Table Mountain Media"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    # Supports both new creation and existing validation catches
    assert response.status_code in [200, 400]

def test_payfast_checkout_generation():
    payload = {
        "amount": 750.00,
        "user_email": "billing@studio.co.za"
    }
    response = client.post("/api/v1/billing/checkout/payfast", json=payload)
    assert response.status_code == 200
    assert "sandbox.payfast.co.za" in response.json()["redirect_url"]
