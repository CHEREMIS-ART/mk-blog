from src.app.services.email import send_email
from src.app.tasks.celery_app import celery_app


@celery_app.task(name="src.app.tasks.email.send_registration_email")
def send_registration_email(email: str, full_name: str | None = None) -> None:
    name = full_name or "друг"
    subject = "Успешная регистрация"
    body = f"Привет, {name}!\n\nВы успешно зарегистрировались в блоге маркетплейса."
    send_email(email, subject, body)
