import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_email(subject, recipient, html_content=None, text_content=None):
    """Send email using Django's configured email backend."""
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@codexio.test")

    if not text_content and html_content:
        text_content = "Please view this email in an HTML-compatible client."

    try:
        send_mail(
            subject,
            text_content or "",
            from_email,
            [recipient],
            html_message=html_content,
            fail_silently=False,
        )
    except Exception as exc:
        logger.error(f"Failed to send email to {recipient}: {str(exc)}")
        raise