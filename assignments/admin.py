from django.contrib import admin

# Register your models here.
from .models import Assignment, Submission

admin.site.register(Assignment)
admin.site.register(Submission)