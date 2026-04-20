from django.db import models
from datetime import timedelta
from django.utils.timezone import now



# Create your models here.


class Update(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return 'code: ' + str(self.timestamp)

    @property
    def deletes_in_ten_seconds(self):
        time = self.timestamp + timedelta(seconds=10)
        query = Update.objects.get(pk=self.pk)
        
        while True:
            if time > now():
                query.delete()
                break

class Message(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)