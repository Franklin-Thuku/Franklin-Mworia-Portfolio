import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime, JSON
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    slug = Column(String(100), unique=True, index=True, nullable=False)
    serial_tag = Column(String(50), nullable=False)  # e.g., "CASE STUDY // 01"
    category = Column(String(100), nullable=False)   # e.g., "SECURITY & INFRASTRUCTURE"
    category_slug = Column(String(50), index=True, nullable=False)  # e.g., "security backend"
    
    title = Column(String(200), nullable=False)
    lead = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    
    # Key Architectural Metrics stored as list of dicts: [{"label": "...", "val": "..."}]
    metrics = Column(JSON, default=list)
    
    # List of strings e.g. ["Go", "Redis", "Docker"]
    technologies = Column(JSON, default=list)
    
    # Architectural Topology Steps for visual preview
    topology = Column(JSON, default=dict)
    
    github_url = Column(String(255), nullable=True)
    demo_url = Column(String(255), nullable=True)
    is_featured = Column(Boolean, default=True, index=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Project {self.slug} - {self.title}>"
