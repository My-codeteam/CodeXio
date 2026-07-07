# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect

from users.models import User, StudentReputation

from courses.models import CompletedCourse, Certificate

from .services import get_student_contributions

from django.db.models import F

from django.core.mail import send_mail

from django.conf import settings

from django.contrib import messages

def book_call(request):

    selected_ids = request.session.get("selected_students", [])

    students = User.objects.filter(id__in=selected_ids)

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        company = request.POST.get("company")
        message = request.POST.get("message")

        student_names = ", ".join([s.fullname for s in students])

        full_message = f"""
Recruitment Request

Name: {name}
Email: {email}
Company: {company}

Selected Students:
{student_names}

Message:
{message}
"""

        send_mail(
            subject="New Recruitment Request - CodexMingle",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
        )

        messages.success(
            request,
            "Thank you! Your request has been sent. We will get back to you shortly."
        )

        request.session["selected_students"] = []

        return redirect("recruit_home")

    return render(request, "recruit/book_call.html", {
        "students": students
    })


LEVEL_MAP = {
    "elite": 800,
    "expert": 500,
    "professional": 250,
    "builder": 100,
    "explorer": 0,
}


def recruit_home(request):

    level = request.GET.get("level")  # filter

    performers = (
        StudentReputation.objects
        .select_related("user")
        .filter(user__is_verified=True)
        .exclude(user__profile_image="")
        .order_by("-total_score")
    )

    # FILTER BY LEVEL
    if level in LEVEL_MAP:
        min_score = LEVEL_MAP[level]

        performers = performers.filter(
            total_score__gte=min_score
        )

    performers = performers[:50]

    latest_certificates = {}

    for p in performers:
        latest_certificates[p.user.id] = (
            Certificate.objects
            .filter(student=p.user)
            .order_by("-issued_date")
            .first()
        )

    request.session.setdefault("selected_students", [])
    selected = request.session["selected_students"]

    return render(request, "recruit/top_performers.html", {
        "performers": performers,
        "latest_certificates": latest_certificates,
        "selected_level": level,
        "selected": selected
    })


def talent_detail(request, username):

    student = get_object_or_404(
        User,
        username=username
    )

    reputation = get_object_or_404(
        StudentReputation,
        user=student
    )

    certificates = (

        Certificate.objects

        .filter(student=student)

        .order_by("-issued_date")

    )

    completed_courses = CompletedCourse.objects.filter(
        user=student
    )

    repositories = get_student_contributions(
    student.github_username
    )


    context = {

        "student": student,

        "reputation": reputation,

        "certificates": certificates,

        "completed_courses": completed_courses,

        "repositories": repositories

    }

    return render(
        request,
        "recruit/talent_detail.html",
        context
    )


def toggle_student(request, user_id):
    request.session.setdefault("selected_students", [])

    selected = request.session.get("selected_students", [])

    if user_id in selected:
        selected.remove(user_id)
    else:
        selected.append(user_id)

    request.session["selected_students"] = selected

    return redirect("recruit_home")