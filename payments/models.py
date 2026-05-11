from django.db import models

# Create your models here.
from django.db import models
from users.models import User
from courses.models import Course

class Payment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=8, decimal_places=2)

    reference = models.CharField(max_length=200)

    status = models.CharField(max_length=20)

    created = models.DateTimeField(auto_now_add=True)