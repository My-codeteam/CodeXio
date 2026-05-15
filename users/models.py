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

            last_user = User.objects.order_by('-id').first()

            if last_user and last_user.student_id:
                last_number = int(last_user.student_id.split("-")[-1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.student_id = f"CM-{year}-{new_number:04d}"

        super().save(*args, **kwargs)