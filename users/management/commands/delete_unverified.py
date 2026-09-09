from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from users.models import User

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        cutoff = timezone.now() - timedelta(minutes=10)

        User.objects.filter(
            is_verified=False,
            date_joined__lt=cutoff
        ).delete()