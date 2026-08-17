import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


async def send_contact_notification(
    name: str,
    email: str,
    inquiry_type: str,
    message: str,
    inquiry_id: str,
    ip_address: str = "Unknown"
) -> bool:
    """
    Sends an email notification to Franklin Thuku (brookthuku@gmail.com)
    when a new portfolio inquiry is submitted.
    Runs asynchronously inside FastAPI BackgroundTasks.
    """
    recipient = settings.NOTIFICATION_EMAIL
    subject = f"[Portfolio Inquiry] New message from {name} ({inquiry_type})"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body {{ font-family: 'Helvetica Neue', Arial, sans-serif; background-color: #09090b; color: #ffffff; padding: 24px; }}
        .card {{ background-color: #141417; border: 1px solid #323238; border-radius: 6px; padding: 24px; max-width: 600px; margin: 0 auto; }}
        .badge {{ background-color: #ffffff; color: #09090b; padding: 4px 8px; font-size: 11px; font-weight: bold; border-radius: 2px; text-transform: uppercase; }}
        .meta-row {{ margin: 12px 0; border-bottom: 1px dashed #27272a; padding-bottom: 8px; }}
        .meta-label {{ color: #a1a1aa; font-size: 12px; text-transform: uppercase; font-family: monospace; }}
        .meta-val {{ color: #ffffff; font-size: 14px; font-weight: 600; margin-top: 2px; }}
        .msg-box {{ background-color: #18181c; border-left: 3px solid #ffffff; padding: 14px; margin-top: 16px; font-size: 14px; line-height: 1.6; white-space: pre-wrap; color: #e4e4e7; }}
        .btn {{ display: inline-block; background-color: #ffffff; color: #09090b; text-decoration: none; padding: 10px 18px; border-radius: 4px; font-weight: bold; font-size: 13px; margin-top: 20px; }}
      </style>
    </head>
    <body>
      <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 16px;">
          <span class="badge">NEW PORTFOLIO INQUIRY</span>
          <span style="color:#71717a; font-size:12px; font-family:monospace;">ID: {inquiry_id[:8]}</span>
        </div>

        <div class="meta-row">
          <div class="meta-label">Sender Name</div>
          <div class="meta-val">{name}</div>
        </div>

        <div class="meta-row">
          <div class="meta-label">Sender Email</div>
          <div class="meta-val"><a href="mailto:{email}" style="color:#ffffff;">{email}</a></div>
        </div>

        <div class="meta-row">
          <div class="meta-label">Classification</div>
          <div class="meta-val">{inquiry_type}</div>
        </div>

        <div class="meta-row">
          <div class="meta-label">Client IP / Origin</div>
          <div class="meta-val" style="font-family:monospace; font-size:12px; color:#a1a1aa;">{ip_address}</div>
        </div>

        <div style="margin-top: 16px;">
          <div class="meta-label">Message Payload</div>
          <div class="msg-box">{message}</div>
        </div>

        <div style="margin-top: 24px;">
          <a href="mailto:{email}?subject=Re:%20{inquiry_type}%20—%20Franklin%20Thuku" class="btn">Reply Directly to {name} →</a>
        </div>
      </div>
    </body>
    </html>
    """

    # If SMTP credentials are configured, dispatch real email
    if settings.SMTP_HOST and settings.SMTP_USER and settings.SMTP_PASSWORD:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"Portfolio System <{settings.SMTP_USER}>"
            msg["To"] = recipient
            msg["Reply-To"] = email

            part_html = MIMEText(html_content, "html")
            msg.attach(part_html)

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                if settings.SMTP_TLS:
                    server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.sendmail(settings.SMTP_USER, recipient, msg.as_string())
            print(f"[EMAIL SERVICE] Successfully dispatched alert to {recipient}")
            return True
        except Exception as e:
            print(f"[EMAIL SERVICE ERROR] Failed to send email via SMTP: {e}")
            return False
    else:
        # Development Console Dispatch Log
        print("\n" + "="*60)
        print(f"[DEV EMAIL LOG] Notification sent to: {recipient}")
        print(f"From: {name} <{email}>")
        print(f"Subject: {subject}")
        print(f"Message: {message}")
        print("="*60 + "\n")
        return True
