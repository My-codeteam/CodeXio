from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Module, Enrollment, Progress, Attendance, ClassSession, Certificate
from assignments.models import Assignment, Submission
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.utils.timezone import now
from .utils import generate_certificate
import pdfkit
from django.http import HttpResponse

def course_list(request):

    search = request.GET.get("search")
    free = request.GET.get("free")

    courses = Course.objects.filter(course_type="recorded")

    if request.user.is_authenticated:
        enrollments = Enrollment.objects.filter(
            user=request.user,
            course=OuterRef("pk")
        )

        courses = courses.annotate(
            enrolled=Exists(enrollments)
        )

    if search:
        courses = courses.filter(title__icontains=search)

    if free:
        courses = courses.filter(price=0)

    context = {
        "courses": courses
    }

    return render(request, "courses/course_list.html", context)


def course_detail(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    modules = course.modules.all()

    assignments = Assignment.objects.filter(module__course=course)

    submissions = Submission.objects.filter(
        student=request.user,
        assignment__in=assignments
    )

    progress = Progress.objects.filter(
        user=request.user,
        course=course
    )

    # Attendance for live courses

    sessions = ClassSession.objects.filter(module__course=course)

    attended_sessions = Attendance.objects.filter(
        student=request.user,
        attended=True
    ).values_list('session_id', flat=True)


    enrolled_course = []

    if request.user.is_authenticated:
        enrolled_course = Enrollment.objects.filter(
            user=request.user
    ).values_list("course_id", flat=True)

    context = {
        "course": course,
        "modules": modules,
        "enrolled_course": enrolled_course,
        "progress": progress,
        "submissions": submissions,
        "assignments": assignments,
        "sessions": sessions,
        'attended_sessions':attended_sessions,
        'now':now()
    }

    return render(request, "courses/course_detail.html", context)


def module_detail(request, module_id):

    module = get_object_or_404(Module, id=module_id)

    course = module.course

    assignment = Assignment.objects.filter(module=module).first()

    enrolled = False

    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(
            user=request.user,
            course=course
        ).exists()

    if course.price > 0 and not enrolled:
        return redirect("initiate_payment", course_id=course.id)

    context = {
        "module": module,
        "assignment": assignment
    }

    return render(request, "courses/course_modules.html", context)

def complete_module(request, module_id):

    module = Module.objects.get(id=module_id)

    Progress.objects.get_or_create(
        user=request.user,
        course=module.course,
        module=module,
        completed=True
    )

    return redirect("course_detail", course_id=module.course.id)


@login_required
def enroll_course(request, course_id):

    course = Course.objects.get(id=course_id)

    # If free course
    if course.price == 0:

        Enrollment.objects.get_or_create(
            user=request.user,
            course=course
        )

        return redirect("course_detail", course_id=course.id)

    # If paid course → redirect to payment
    else:
        return redirect("payments:initiate_payment", course_id=course.id)


@login_required
def submit_assignment(request, assignment_id):

    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.method == "POST":

        file = request.FILES.get("file")

        Submission.objects.update_or_create(
            assignment=assignment,
            student=request.user,
            defaults={
                "file": file
            }
        )

    return redirect("courses:course_detail", course_id=assignment.module.course.id)

def certificate_view(request, course_id):

    certificate = generate_certificate(request.user, course_id)

    if not certificate:
        return HttpResponse("Course not completed yet")

    return render(
        request,
        "courses/certificates/certificate.html",
        {"certificate": certificate}
    )


def download_certificate(request, certificate_id):

    certificate = get_object_or_404(
        Certificate,
        certificate_id=certificate_id
    )

    html = render(
        request,
        "courses/certificates/certificate_pdf.html",
        {"certificate": certificate}
    ).content.decode("utf-8")

    pdf = pdfkit.from_string(html, False)

    response = HttpResponse(
        pdf,
        content_type="application/pdf"
    )

    response['Content-Disposition'] = f'attachment; filename="certificate.pdf"'

    return response


def verify_certificate(request, certificate_id):

    certificate = get_object_or_404(
        Certificate,
        certificate_id=certificate_id
    )

    return render(
        request,
        "courses/certificates/verify.html",
        {"certificate": certificate}
    )
