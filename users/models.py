from django.db import models
from django.utils.timezone import now
from django.conf import settings

# Create your models here.
from django.contrib.auth.models import AbstractUser

import uuid

class User(AbstractUser):

    student_id = models.CharField(max_length=20, unique=True, blank=True)
    fullname = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    github_username = models.CharField(
    max_length=100,
    blank=True,
    null=True
    )
    profile_image = models.ImageField(upload_to='profiles/', blank=True)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(
    null=True,
    blank=True
    )

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

        if not self.github_username:

            self.github_username = self.username


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


class StudentReputation(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    completed_courses = models.IntegerField(default=0)

    github_contributions = models.IntegerField(default=0)

    assignments_submitted = models.IntegerField(default=0)

    live_attendance = models.IntegerField(default=0)

    mentor_sessions = models.IntegerField(default=0)

    total_score = models.IntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def calculate_score(self):

        self.total_score = (

            (self.completed_courses * 10)

            +

            (self.github_contributions * 1)

            +

            (self.assignments_submitted * 2)

            +

            (self.live_attendance * 3)

            +

            (self.mentor_sessions * 5)

        )

        self.save()

    def __str__(self):
        return f"{self.user.username} Reputation"

    @property
    def badge(self):

        if self.total_score >= 800:
           return "🏆 Elite Developer"

        elif self.total_score >= 500:
           return "⭐ Expert Developer"

        elif self.total_score >= 250:
           return "🚀 Professional Developer"

        elif self.total_score >= 100:
           return "🔨 Builder"

        return "🌱 Explorer"