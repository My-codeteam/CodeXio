from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from users.models import User

from django.db.models import Q

class Command(BaseCommand):
    help = "Delete users inactive for more than 4 months."

    def handle(self, *args, **kwargs):

        cutoff = timezone.now() - timedelta(days=120)

        User.objects.filter(
          is_staff=False,
          is_superuser=False
        ).filter(
          Q(last_login__lt=cutoff) |
          Q(last_login__isnull=True, date_joined__lt=cutoff)
        ).delete()