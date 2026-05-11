from django.db import models

# Create your models here.

from users.models import User

class Course(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    price = models.DecimalField(max_digits=8, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)


class Module(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")

    title = models.CharField(max_length=200)

    content = models.TextField()

    order = models.IntegerField()


class Enrollment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    paid = models.BooleanField(default=False)

    enrolled_at = models.DateTimeField(auto_now_add=True)


class Progress(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    completed = models.BooleanField(default=False)