from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model

from .models import StudentReputation

User = get_user_model()


@receiver(post_save, sender=User)
def create_reputation(sender, instance, created, **kwargs):

    if created:

        StudentReputation.objects.create(
            user=instance
        )