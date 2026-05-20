from django.contrib import admin
from .models import Course, Module, ModuleAccess, Enrollment, Progress, UpdateNotification, Attendance, CompletedCourse, Certificate
# Register your models here.
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Enrollment)
admin.site.register(Progress)
admin.site.register(UpdateNotification)
admin.site.register(CompletedCourse)
admin.site.register(Certificate)
admin.site.register(ModuleAccess)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = ('student','session','attended')

    list_filter = ('attended',)