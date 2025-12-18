import smtplib
from email.message import EmailMessage

from src.app.core.config import settings


def send_email(to: str, subject: str, body: str) -> None:
    if settings.ENV == "test":
        return

    msg = EmailMessage()
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
        try:
            server.starttls()
        except smtplib.SMTPException:
            pass

        if settings.EMAIL_USER and settings.EMAIL_PASSWORD:
            server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)

        server.send_message(msg)
