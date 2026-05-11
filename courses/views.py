from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Module, Enrollment, Progress
from assignments.models import Assignment


def course_list(request):

    search = request.GET.get("search")
    free = request.GET.get("free")

    courses = Course.objects.all()

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

    enrolled = False

    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(
            user=request.user,
            course=course
        ).exists()

    context = {
        "course": course,
        "modules": modules,
        "enrolled": enrolled
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

    return redirect("course_modules", id=module.course.id)