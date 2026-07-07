import resend
from django.conf import settings

resend.api_key = settings.RESEND_API_KEY


def send_email(subject, recipient, html_content=None, text_content=None):

    params = {
        "from": f"CodexMingle <{settings.DEFAULT_FROM_EMAIL}>",
        "to": recipient,
        "subject": subject,
    }

    if html_content:
        params["html"] = html_content

    if text_content:
        params["text"] = text_content

    resend.Emails.send(params)