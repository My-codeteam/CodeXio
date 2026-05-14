from django.db import models

# Create your models here.

from users.models import User
from courses.models import Course, Module

class Assignment(models.Model):

    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    description = models.TextField()

    is_live = models.BooleanField(default=False)


class Submission(models.Model):

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)

    student = models.ForeignKey(User, on_delete=models.CASCADE)

    file = models.FileField(upload_to='submissions/')

    grade = models.CharField(max_length=10, blank=True)

    feedback = models.TextField(blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['assignment', 'student']