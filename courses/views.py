from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Module, Enrollment, Progress, Attendance, ClassSession, Certificate, CompletedCourse, MentorRequest, ModuleAccess
from assignments.models import Assignment, Submission
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.utils.timezone import now
from .utils import generate_certificate
import pdfkit
from django.http import HttpResponse
import random
import string
from django.utils import timezone
from datetime import timedelta
from users.models import User
from decimal import Decimal
from users.models import StudentReputation
from .forms import MentorRequestForm
from django.contrib import messages


@login_required
def course_list(request):

    search = request.GET.get("search")
    free = request.GET.get("free")

    courses = Course.objects.filter(course_type="recorded")


    # COURSE DISCOUNT

    # FIRST 200 USERS DISCOUNT
    total_users = User.objects.count()

    for course in courses:

        final_price_fee = course.price

        discounted_amount = (Decimal(course.discount_percentage) / Decimal("100")) * final_price_fee

        # NORMAL COURSE DISCOUNT
        if (
            course.discount_active and
            course.discount_expiry and
            timezone.now() < course.discount_expiry
        ):

            final_price =  final_price_fee - discounted_amount

        # FIRST 200 USERS DISCOUNT
        if total_users <= 200:

            final_price = final_price_fee - discounted_amount

        # attach dynamically
        course.final_price = final_price

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
        "courses": courses,
        "final_price": final_price,
        "final_price_fee": final_price_fee
    }

    return render(request, "courses/course_list.html", context)


@login_required
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

    total_modules = modules.count()

    # COMPLETED MODULES BY USER
    completed_modules = progress.filter(completed=True).count()

    # Check if course is completed
    if total_modules > 0 and completed_modules == total_modules:

        CompletedCourse.objects.get_or_create(
            user=request.user,
            course=course
        )

        reputation, created = StudentReputation.objects.get_or_create(
         user=request.user
        )

        reputation.completed_courses += 1

        reputation.calculate_score()

        # Generate formatted certificate ID
        year = timezone.now().year

        course_code = course.title[:2].upper()

        random_hash = ''.join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=5
            )
        )

        formatted_id = f"CM-{year}-{course_code}-{random_hash}"

        Certificate.objects.get_or_create(
            student=request.user,
            course=course,
            certificate_type="completion",
            defaults={
                "certificate_id": formatted_id
            }
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

    total_sessions = sessions.count()

    attended_count = Attendance.objects.filter(
        student=request.user,
        session__in=sessions,
        attended=True
    ).count()

    attendance_percent = 0

    if total_sessions > 0:
        attendance_percent = (attended_count / total_sessions) * 100

    mentor_remaining = MentorRequest.remaining_sessions(
    request.user,
    course
    )

    context = {
        "course": course,
        "modules": modules,
        "enrolled_course": enrolled_course,
        "progress": progress,
        "submissions": submissions,
        "assignments": assignments,
        "sessions": sessions,
        'attended_sessions':attended_sessions,
        'now':now(),
        "mentor_remaining": mentor_remaining,
        "attendance_percent": attendance_percent
    }

    return render(request, "courses/course_detail.html", context)


@login_required
def module_detail(request, module_id):

    module = get_object_or_404(Module, id=module_id)

    course = module.course

    assignment = Assignment.objects.filter(module=module).first()

    enrolled = False

    access, created = ModuleAccess.objects.get_or_create(
        user=request.user,
        module=module,
        defaults={
            "deadline": timezone.now() + timedelta(days=5)
        }
    )

    submitted = Submission.objects.filter(
    student=request.user,
    assignment__module=module
    )

    total_assignments = Assignment.objects.filter(
    module=module
    ).count()

    if submitted.count() == total_assignments and total_assignments > 0:

        Progress.objects.get_or_create(
            user=request.user,
            course=module.course,
            module=module,
            defaults={
               "completed": True
            }
        )

    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(
            user=request.user,
            course=course
        ).exists()

    if course.price > 0 and not enrolled:
        return redirect("initiate_payment", course_id=course.id)

    context = {
        "module": module,
        "course": course,
        "assignment": assignment,
        "deadline": access.deadline
    }

    return render(request, "courses/course_modules.html", context)

@login_required
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

        link = request.FILES.get("link")

        Submission.objects.update_or_create(
            assignment=assignment,
            student=request.user,
            defaults={
                "link": link
            }
        )
    reputation, created = StudentReputation.objects.get_or_create(
    user=request.user
    )

    reputation.assignments_submitted += 1

    reputation.calculate_score()

    return redirect("course_detail", course_id=assignment.module.course.id)

@login_required
def certificate_view(request, completed_id):

    completed = get_object_or_404(
        CompletedCourse,
        id=completed_id,
        user=request.user
    )

    certificate = generate_certificate(
        request.user,
        completed.course.id
    )

    if not certificate:
        return HttpResponse("Course not completed yet")

    return render(
        request,
        "courses/certificates/certificate.html",
        {"certificate": certificate}
    )


@login_required
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

@login_required
def my_certificates(request):

    certificates = CompletedCourse.objects.filter(
        user=request.user
    ).select_related("course")

    context = {
        "certificates": certificates
    }

    return render(
        request,
        "courses/certificates/my_certificates.html",
        context
    )


@login_required
def request_mentor(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    remaining = MentorRequest.remaining_sessions(
        request.user,
        course
    )

    if remaining <= 0:

        messages.error(
            request,
            "You have used all mentor sessions."
        )

        return redirect(
            "course_detail",
            course_id=course.id
        )

    if request.method == "POST":

        form = MentorRequestForm(request.POST)

        if form.is_valid():

            mentor_request = form.save(
                commit=False
            )

            mentor_request.user = request.user

            mentor_request.course = course

            mentor_request.save()

            messages.success(
                request,
                "Request submitted successfully."
            )

            return redirect(
                "course_detail",
                course_id=course.id
            )

    else:

        form = MentorRequestForm()

    return render(
        request,
        "courses/request_mentor.html",
        {
            "form": form,
            "course": course,
            "remaining": remaining
        }
    )
