from django.db import models

# Create your models here.
from django.db import models
from users.models import User
from courses.models import Course, Enrollment

class Payment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    receipt = models.ImageField(upload_to="payment_receipts/", null=True, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

      super().save(*args, **kwargs)

      if self.verified and not Enrollment.objects.filter(user=self.user, course=self.course).exists():

        Enrollment.objects.create(
            user=self.user,
            course=self.course,
            paid=True
        )

class Meta:
    unique_together = ["user", "course"]