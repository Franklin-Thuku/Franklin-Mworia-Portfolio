from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ContactMessageCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="Sarah Jenkins")
    email: EmailStr = Field(..., example="sarah.jenkins@company.com")
    inquiry_type: str = Field(default="General Inquiry", max_length=100, example="Custom MVP / Backend Build")
    message: str = Field(..., min_length=5, max_length=5000, example="Hi Franklin, we are looking for a backend engineer...")
    
    # Honeypot field (hidden from real users; if filled, bot is detected)
    website_url_hp: Optional[str] = Field(default=None, max_length=50)


class ContactMessageResponse(BaseModel):
    id: str
    name: str
    email: str
    inquiry_type: str
    message: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ContactSuccessResponse(BaseModel):
    status: str = "success"
    message: str
    inquiry_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
