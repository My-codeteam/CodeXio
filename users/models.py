from django.db import models
from django.utils.timezone import now

# Create your models here.
from django.contrib.auth.models import AbstractUser

import uuid

class User(AbstractUser):

    student_id = models.CharField(max_length=20, unique=True, blank=True)

    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    profile_image = models.ImageField(upload_to='profiles/', blank=True)

    def save(self, *args, **kwargs):

        if not self.student_id:
            year = now().year
            count = User.objects.count() + 1
            self.student_id = f"CM-{year}-{count:04d}"

        super().save(*args, **kwargs)