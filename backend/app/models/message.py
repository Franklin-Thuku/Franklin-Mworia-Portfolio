import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime
from app.core.database import Base


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    inquiry_type = Column(String(100), nullable=False, default="General Inquiry")
    message = Column(Text, nullable=False)
    
    # Telemetry & Security Audit Metadata
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    
    is_read = Column(Boolean, default=False, index=True)
    is_archived = Column(Boolean, default=False, index=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<ContactMessage from {self.name} ({self.email})>"
