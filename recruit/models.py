# Create your models here.

from django.db import models
from django.conf import settings


class RecruitRequest(models.Model):

    recruiter_name = models.CharField(max_length=100)
    recruiter_email = models.EmailField()
    company = models.CharField(max_length=100, blank=True)

    message = models.TextField(blank=True)

    selected_students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="recruit_requests"
    )

    level_filter = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        default="pending"
    )

    def __str__(self):
        return f"{self.recruiter_name} - {self.created_at}"