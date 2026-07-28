import os
from sqlalchemy import create_backend, create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

# Local SQLite fallback engine if PostgreSQL environment string is absent
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./studio_workspace.db")

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialises global schema constraints and structure on storage systems."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Yields clean localized transaction boundaries for active requests."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
