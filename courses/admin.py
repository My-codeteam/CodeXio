from django.contrib import admin
from .models import MentorRequest, Course, Module, ModuleAccess, Enrollment, Progress, UpdateNotification, Attendance, CompletedCourse, Certificate, ClassSession
# Register your models here.
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Enrollment)
admin.site.register(Progress)
admin.site.register(UpdateNotification)
admin.site.register(CompletedCourse)
admin.site.register(Certificate)
admin.site.register(ModuleAccess)
admin.site.register(ClassSession)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = ('student','session','attended')

    list_filter = ('attended',)


@admin.register(MentorRequest)
class MentorRequestAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "course",
        "status",
        "created_at"
    )

    list_filter = (
        "status",
        "course"
    )