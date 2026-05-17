from django.contrib import admin
from .models import Course, Module, Enrollment, Progress, UpdateNotification, Attendance
# Register your models here.
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Enrollment)
admin.site.register(Progress)
admin.site.register(UpdateNotification)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = ('student','session','attended')

    list_filter = ('attended',)