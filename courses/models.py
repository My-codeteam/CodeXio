from django.db import models
from django.utils.text import slugify
from datetime import timedelta
from django.utils.timezone import now
from codexio_main.models import Update
import uuid
import random
import string
# Create your models here.

from users.models import User

class Course(models.Model):
    COURSE_TYPE = (
        ("recorded", "Recorded"),
        ("live", "Live"),
    )

    PAYMENT_TYPE = (
        ('transfer', 'transfer'),
        ('mastercard',  'Mastercard')
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    price = models.DecimalField(max_digits=8, decimal_places=2)

    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE, default="transfer")

    course_type = models.CharField(
        max_length=10,
        choices=COURSE_TYPE,
        default="recorded"
    )

    enrollment_open = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


class Module(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")

    title = models.CharField(max_length=200)

    content = models.TextField()

    order = models.IntegerField()

    class_url = models.URLField(blank=True, null=True)

    class_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order"]


class Enrollment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    paid = models.BooleanField(default=False)

    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'course']


class UpdateNotification(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    @property
    def deletes_in_two_days(self):
        time = self.timestamp + timedelta(days=2)
        query = Update.objects.get(pk=self.pk)

        while True:
            if time > now():
                query.delete()
                break


class Progress(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'module']

class ClassSession(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, blank=True)
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

def generate_certificate_code(course):
    year = "2026"

    # course abbreviation
    title = course.title.lower()

    if "backend" in title:
        course_code = "BE"
    elif "frontend" in title:
        course_code = "FE"
    elif "cloud" in title:
        course_code = "CL"
    else:
        course_code = "CR"

    random_hash = ''.join(random.choices(string.hexdigits.upper(), k=5))

    return f"CM-{year}-{course_code}-{random_hash}"


class Certificate(models.Model):

    CERT_TYPE = (
        ("completion", "Completion"),
        ("participation", "Participation"),
        ("achievement", "Achievement"),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    certificate_type = models.CharField(
        max_length=20,
        choices=CERT_TYPE,
        default="completion",
    )

    certificate_id = models.CharField(
        max_length=50,
        unique=True,
        editable=False
    )

    issued_date = models.DateTimeField(auto_now_add=True)

    certificate_template = models.ImageField(
        upload_to="certificate_templates/",
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):

        if not self.certificate_id:
            self.certificate_id = generate_certificate_code(self.course)

        super().save(*args, **kwargs)

    class Meta:
        unique_together = ['student', 'course', 'certificate_type']

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"

class CompletedCourse(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "course"]

    def __str__(self):
        return f"{self.user.username} completed {self.course.title}"
