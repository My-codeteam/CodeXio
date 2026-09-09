from unittest.mock import patch
from django.test import SimpleTestCase

from services.resend_service import send_email


class SendEmailTests(SimpleTestCase):
    @patch("django.core.mail.send_mail")
    def test_send_email_uses_django_backend_when_resend_key_missing(self, mock_send_mail):
        with self.settings(RESEND_API_KEY="", DEFAULT_FROM_EMAIL="noreply@example.com"):
            send_email("Subject", "user@example.com", "<p>Hi</p>", "Plain text")

        mock_send_mail.assert_called_once_with(
            "Subject",
            "Plain text",
            "noreply@example.com",
            ["user@example.com"],
            html_message="<p>Hi</p>",
            fail_silently=False,
        )
