# 📁 app/core/email_service.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings


def send_verification_email(email: str, user_id: int):
    subject = "Verify Your Email Address"
    verification_link = f"{settings.FRONTEND_BASE_URL}/verify-email?user_id={user_id}"

    html_content = f"""
    <html>
      <body>
        <p>Hello 👋,<br>
           Please verify your email by clicking the link below:<br>
           <a href="{verification_link}">Verify Email</a>
        </p>
        <p>If you didn’t create this account, you can ignore this email.</p>
      </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_SENDER
    msg["To"] = email

    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_SENDER, email, msg.as_string())
    except Exception as e:
        raise RuntimeError(f"Failed to send verification email: {e}")
