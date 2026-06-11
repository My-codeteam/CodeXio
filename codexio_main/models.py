from django.db import models
from datetime import timedelta
from django.utils.timezone import now
from users.models import User


# Create your models here.


class Update(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'code: ' + str(self.timestamp)

    @property
    def deletes_in_two_days(self):
        time = self.timestamp + timedelta(days=2)
        query = Update.objects.get(pk=self.pk)

        while True:
            if time > now():
                query.delete()
                break

class Message(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    subject = models.CharField(
        max_length=200
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    resolved = models.BooleanField(
        default=False
    )