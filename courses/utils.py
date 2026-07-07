from courses.models import Progress
from .models import Certificate, CompletedCourse, Module


def generate_certificate(user, course):

    modules = Module.objects.filter(course=course)

    completed = Progress.objects.filter(
        user=user,
        course=course,
        completed=True
    ).count()

    total = modules.count()

    if completed == total and total != 0:

        certificate, created = Certificate.objects.get_or_create(
            student=user,
            course=course,
            certificate_type="completion"
        )

        CompletedCourse.objects.get_or_create(
            user=user,
            course=course
        )

        return certificate

    return None