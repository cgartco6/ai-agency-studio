from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.api import auth, billing, scraper, generator

# Initialize FastAPI Engine
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for cross-origin frontend browser queries
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to specific production domains as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# On-Startup Database Activation Hook
@app.on_event("startup")
def on_startup():
    print("[SYSTEM LOG]: Activating Database Schema Foundations...")
    init_db()
    print("[SYSTEM LOG]: Database tables confirmed. Studio engine operational.")

# Mount Core Module Sub-Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(billing.router, prefix=settings.API_V1_STR)
app.include_router(scraper.router, prefix=settings.API_V1_STR)
app.include_router(generator.router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {
        "status": "Online",
        "system": settings.PROJECT_NAME,
        "default_currency": settings.DEFAULT_CURRENCY
    }
