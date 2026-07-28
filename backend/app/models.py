from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class UserWorkspace(Base):
    __tablename__ = "user_workspaces"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    currency = Column(String, default="ZAR")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    leads = relationship("ScrapedLead", back_populates="workspace")
    assets = relationship("GeneratedAsset", back_populates="workspace")

class ScrapedLead(Base):
    __tablename__ = "scraped_leads"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("user_workspaces.id"), nullable=False)
    company_name = Column(String, nullable=False)
    website = Column(String)
    email = Column(String)
    location = Column(String)
    status = Column(String, default="Cold Lead Found")
    scraped_at = Column(DateTime, default=datetime.utcnow)

    workspace = relationship("UserWorkspace", back_populates="leads")

class GeneratedAsset(Base):
    __tablename__ = "generated_assets"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("user_workspaces.id"), nullable=False)
    brand_name = Column(String, nullable=False)
    tagline = Column(String)
    primary_color = Column(String)
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    workspace = relationship("UserWorkspace", back_populates="assets")
