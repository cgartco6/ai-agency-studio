import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Design, Branding & Marketing Studio"
    API_V1_STR: str = "/api/v1"
    
    # Currency Configurations
    DEFAULT_CURRENCY: str = "ZAR"
    
    # Gateways API Keys (Loaded from environment variables)
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "sk_test_mock")
    PAYFAST_MERCHANT_ID: str = os.getenv("PAYFAST_MERCHANT_ID", "mock_id")
    PAYFAST_MERCHANT_KEY: str = os.getenv("PAYFAST_MERCHANT_KEY", "mock_key")
    PAYPAL_CLIENT_ID: str = os.getenv("PAYPAL_CLIENT_ID", "mock_paypal_id")
    PAYPAL_SECRET: str = os.getenv("PAYPAL_SECRET", "mock_paypal_secret")
    
    class Config:
        case_sensitive = True

settings = Settings()
