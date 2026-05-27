from django.db import models
from django.utils.timezone import now

# Create your models here.
from django.contrib.auth.models import AbstractUser

import uuid

class User(AbstractUser):

    student_id = models.CharField(max_length=20, unique=True, blank=True)
    fullname = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)

    profile_image = models.ImageField(upload_to='profiles/', blank=True)
    is_verified = models.BooleanField(default=False)

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



class EmailVerification(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True
    )

    verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username