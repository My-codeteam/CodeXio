from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Module, Enrollment, Progress
from assignments.models import Assignment, Submission
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef

def course_list(request):

    search = request.GET.get("search")
    free = request.GET.get("free")

    courses = Course.objects.all()

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
    sessions = course.classsession_set.all()


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
        "sessions": sessions
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