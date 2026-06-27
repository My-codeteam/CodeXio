from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Update)
admin.site.register(Message)
admin.site.register(Feedback)
admin.site.register(SiteVisit)
admin.site.register(Testimonial)