from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.api.deps import get_db
from app.models.message import ContactMessage
from app.schemas.message import ContactMessageCreate, ContactMessageResponse, ContactSuccessResponse
from app.services.email_service import send_contact_notification
from app.services.rate_limiter import contact_rate_limiter

router = APIRouter(prefix="/contact", tags=["Contact & Inquiries"])


@router.post("", response_model=ContactSuccessResponse, status_code=status.HTTP_201_CREATED)
async def submit_contact_inquiry(
    inquiry_in: ContactMessageCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Public endpoint for portfolio visitors to send questions or contract inquiries.
    Includes rate limiting, honeypot spam protection, database persistence,
    and non-blocking email notification dispatch.
    """
    # 1. Extract Client Metadata
    client_ip = request.client.host if request.client else "127.0.0.1"
    # Support reverse proxies (e.g., Cloudflare / Nginx / Render)
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0].strip()
    user_agent = request.headers.get("user-agent", "Unknown")[:250]

    # 2. Honeypot Spam Protection Check
    # If the hidden field is filled, it's an automated bot. Silently drop without error.
    if inquiry_in.website_url_hp:
        print(f"[SECURITY] Bot trapped via honeypot from IP: {client_ip}")
        return ContactSuccessResponse(
            status="success",
            message="Transmission received.",
            inquiry_id="00000000-0000-0000-0000-000000000000"
        )

    # 3. IP Rate Limiting Check
    if not contact_rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please wait a few minutes before dispatching another message."
        )

    # 4. Save Inquiry to Database
    new_message = ContactMessage(
        name=inquiry_in.name,
        email=inquiry_in.email,
        inquiry_type=inquiry_in.inquiry_type,
        message=inquiry_in.message,
        ip_address=client_ip,
        user_agent=user_agent
    )
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)

    # 5. Non-Blocking Background Email Alert
    background_tasks.add_task(
        send_contact_notification,
        name=new_message.name,
        email=new_message.email,
        inquiry_type=new_message.inquiry_type,
        message=new_message.message,
        inquiry_id=new_message.id,
        ip_address=client_ip
    )

    return ContactSuccessResponse(
        status="success",
        message="Your message has been logged and dispatched to Franklin Thuku. Expect a response within 12 hours.",
        inquiry_id=new_message.id
    )


@router.get("/messages", response_model=List[ContactMessageResponse])
async def list_contact_messages(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    unread_only: bool = Query(False),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve inbox submissions (used by Admin Dashboard in Phase 3).
    """
    query = select(ContactMessage).order_by(desc(ContactMessage.created_at))
    if unread_only:
        query = query.where(ContactMessage.is_read == False)
        
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()
