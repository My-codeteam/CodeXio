from django.db import models
from django.utils.text import slugify

# Create your models here.

from users.models import User

class Course(models.Model):
    COURSE_TYPE = (
        ("recorded", "Recorded"),
        ("live", "Live"),
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    price = models.DecimalField(max_digits=8, decimal_places=2)

    course_type = models.CharField(
        max_length=10,
        choices=COURSE_TYPE,
        default="recorded"
    )

    created_at = models.DateTimeField(auto_now_add=True)


class Module(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")

    title = models.CharField(max_length=200)

    content = models.TextField()

    order = models.IntegerField()

    class Meta:
        ordering = ["order"]


class Enrollment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    paid = models.BooleanField(default=False)

    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'course']


class Progress(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'module']

class ClassSession(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Attendance(models.Model):

    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    attended = models.BooleanField(default=False)

    class Meta:
        unique_together = ['session', 'student']

