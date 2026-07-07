import nltk

from nltk.chat.util import Chat, reflections
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import *
from users.models import User, EmailVerification, StudentReputation
from django.db.models.functions import Now
from datetime import timedelta
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.db.models import Count

User = get_user_model()
from courses.models import Course, Enrollment, UpdateNotification, Module, CompletedCourse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from assignments.models import Assignment
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import F
# from services.resend_service import send_email

# Download the nltk data if not already downloaded
nltk.download('punkt')

# Define the chatbot patterns and responses

chatbot_pairs = [
    [
        "hello|hi|hey|good day",
        ["Hi. How can I be of help to you?","Hi my friend. How can I be of help to you?",]
    ],
    [
        r"I love you",
        ["Thanks.","Awww...That's so adorable", "That's so nice of you, thanks.",]
    ],
    [
        r"sup|what's up|how are you",
        ["I'm good. What about you?",]
    ],
    [
        r"Tell me about Codexio|Tell me about this website|I would love to know more about Codexio|What is Codexio",
        ["This is a coding/programming community that is aimed at helping like minds grow. We help those aspiring to be developers get to the point of being job ready. We also encourage the spirit of learning and healthy compitition.",]
    ],
    [
        r"Good too|I'm good too|I'm great|I'm fine|I'm doing well",
        ["Good to know","Great!",]
    ],
    [
        r"What do you love doing|What do you like",
        ["I love to help people who are just like me, a computer guru.",]
    ],
    [
        r"What can you do|I don't know, you tell me",
        ["As a Chat bot, I can only understand little human interaction and give you direct answers. I only recognize questions stored in my database for now, so can only chat with you like you are chatting with my makers. I may not understand complex interactions, but will become better overtime. I can also save chats in case of future reference. I could also tell you some jokes, if you want to laugh just type 'make me laugh'.",]
    ],
    [
        r"Why can't you understand me|What can you answer|What are some questions you answer",
        ["Sorry about that. You could try rephrasing the question or sentence. You could watch this video on my commands and how to use me. Here's the link","I only answer questions that relates to this website, me and programming. You could either rephrase the question or ask another question.",]
    ],
    [
        r"Who made you|by whom|by who",
        ["A team of friendly programmers who loves what they do. Together they made this community.",]
    ],
    [
        r"What is their vision|Why was codexio made|why was codexio created",
        ["Their vision is to grow and help as many people as possible.",]
    ],
    [
        r"I would love to ask you some questions|I want ask something|Can I ask you a question|I want to ask something from you|Can I ask",
        ["Sure","Alright",]
    ],
    [
        r"Okay, thanks|Thanks|Thanks a lot|I really appreciate the help|Thank you",
        ["Happy to help","Don't mention it.","You're welcome.",]
    ],
    [
        r"What year were you born|What year were you made|When were you developed",
        ["The year 2023.",]
    ],
    [
        r"Goodbye|Bye|Alright, talk to you later",
        ["Alright, bye","Yeah, bye", "See you soon",]
    ],
    [
        r"nothing for now|nothing",
        ["Alright",]
    ],
    [
        r"Cool|That's nice|That's wonderful|That's extraordinary|That's funny",
        ["Thanks", "All love",]
    ],
    [
        r"Zillo",
        ["Yes. How may I help you?","Hi. How can I help you?",]
    ],
    [
        r"What is your name?",
        ["My name is Zillow your personal chatbot assistant from codexio, created to help you through this website and any updates that comes up. I am also your buddy incase you just want to chat. You want my help you could just enter Zillow.",]
    ],
    [
        r"Okay|Ok",
        ["Yeah...",]
    ],
    [
        r"Tell me a joke|Make me laugh|another joke",
        ["Why don't scientists trust atoms? Because they make up everything!","Parallel lines have so much in common. It's a shame they'll never meet.", "Why did the math book look sad? Because it had too many problems.", "I used to play piano by ear, but now I use my hands.", "Why did the bicycle fall over? Because it was two-tired!"]
    ],
    [
        r"What schools are great for programming|How can I make my programming skills",
        ["These schools are great schools for learning how to code Udemy, Codeacademy, W3Schools, freecodecamp.", "Choose a Programming Language. Learn the Basics. Practice Regularly. Build Projects. Read Code. Join Programming Communities( this step you have already taken).",]
    ],
    [
        r"I am not feeling so",
        ["You are probably ill. Take a rest from what you are doing. All work and no play makes Jack a dull boy.", "I suggest you visit the doctor as quickly as possible.",]
    ],
    [
        r"I have a compliant to make on the website",
        ["All compliant should go to my makers, I can't help with that for now. Here's their email: . You could also give your compliants in the community you're in. So sorry for the inconvenience.",]
    ],
    [
        r"Can you save my chats|Why don't you save my chats",
        ["Right after a reload the chats are cleared, but I save them on the database for quick learning. Only updates made by me would show up for five days, afterward would disappear.",]
    ],
    [
        r"What is the fastest animal in the world",
        ["The Periguim Falcon.", "The Birds.", "This question is not related to this website."]
    ],

    [
        r"(.*)",
        ["I'm sorry, but I don't understand that, and maybe can't answer that question due to some reasons. You could try rephrasing the question or sentence, or asking another question. You could watch this video on my commands and how to use me. Here's the link: . I can only answer questions that relates to this website, me and programming.",]
    ],
]
def home(request):
    visit_obj, _ = SiteVisit.objects.get_or_create(id=1)

    visit_obj.count = F('count') + 1
    visit_obj.save()

    visit_obj.refresh_from_db()

    testimonials = Testimonial.objects.filter(
    approved=True)[:6]
    return render(request, 'codexio_main/index.html', {
        "visits": visit_obj.count, "testimonials": testimonials
    })


def testimonial(request):

    if request.method == "POST":

        Testimonial.objects.create(

            name=request.POST["name"],

            email=request.POST.get("email"),

            country=request.POST["country"],

            rating=request.POST.get("rating", 5),

            comment=request.POST["comment"]

        )

        messages.success(
            request,
            "Thank you! Your review has been submitted and will appear after approval. Please kindly be patient."
        )

        return redirect("/testimonial")

    return render(
        request,
        "codexio_main/testimonial.html"
    )

@login_required
def feedback(request):

    if request.method == "POST":

        subject = request.POST.get("subject")

        message = request.POST.get("message")

        html_content = f"""
<h2>New Feedback Received</h2>

<p><b>From:</b> {request.user.fullname}</p>

<p><b>Username:</b> {request.user.username}</p>

<p><b>Email:</b> {request.user.email}</p>

<hr>

<p>{message}</p>
"""

        send_mail(
            subject=f"[CodexMingle Feedback] {subject}",
            message=f"""
From: {request.user.fullname}
Username: {request.user.username}
Email: {request.user.email}

Message:
{message}
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[
                settings.DEFAULT_FROM_EMAIL
            ],
            fail_silently=False
        )

        Feedback.objects.create(
          user=request.user,
          subject=subject,
          message=message
        )

        messages.success(
            request,
            "Thank you! Your feedback has been sent."
        )

        return redirect("/feedback")

    return render(
        request,
        "codexio_main/feedback.html"
    )

def custom_404(request, exception):
    return render(request, 'codexio_main/404.html', status=404)

def custom_500(request):
    return render(request, 'codexio_main/500.html', status=500)

def about(request):
    return render(request, 'codexio_main/about.html')

def coming_soon(request):
    return render(request, 'codexio_main/coming_soon.html')

def chatbot(request):
    if request.method == 'POST':
        user_message = request.POST.get('content')
        message = Message.objects.create(content=user_message)

        response = get_chatbot_response(user_message)
        Message.objects.create(content=response)

        return JsonResponse({'response': response})
    updates_zillow = Update.objects.all()
    context = {}
    context["updates_zillow"] = updates_zillow

    # Update.objects.filter(timestamp__lt=Now()-timestamp(days=5)).delete()


    return render(request, 'codexio_main/chatbot.html', context)

def get_chatbot_response(user_message):
    chatbot = Chat(chatbot_pairs, reflections)
    return chatbot.respond(user_message)

@login_required
def student_portal(request):
    contributors = []

    try:

        url = "https://api.github.com/repos/codexmingleteam-sudo/student-projects/contributors"

        response = requests.get(url)

        if response.status_code == 200:

            contributors = response.json()[:10]

            # Update GitHub contributions in reputation table
            for contributor in contributors:

                github_name = contributor["login"]

                contributions = contributor["contributions"]

                try:

                    user = User.objects.get(
                        github_username=github_name
                    )

                    reputation, created = StudentReputation.objects.get_or_create(
                        user=user
                    )

                    reputation.github_contributions = contributions

                    reputation.calculate_score()

                except User.DoesNotExist:

                    pass

    except Exception:

        contributors = []


    total_courses = Course.objects.count()

    total_members = User.objects.count()

    courses_enrolled = Enrollment.objects.filter(
        user=request.user
    ).count()

    courses = Course.objects.order_by("-id")[:6]

    updates = UpdateNotification.objects.all()


    # GitHub repos count
    total_repos = 0

    try:

        url = "https://api.github.com/users/codexmingleteam-sudo/repos"

        response = requests.get(url)

        if response.status_code == 200:

            repos = response.json()

            total_repos = len(repos)

    except Exception:

        pass


    # Leaderboard
    top_students = StudentReputation.objects.select_related(
        "user"
    ).filter(
       total_score__gt=0
    ).order_by(
        "-total_score"
    )[:10]


    context = {

        "total_courses": total_courses,

        "total_members": total_members,

        "courses_enrolled": courses_enrolled,

        "total_repos": total_repos,

        "updates": updates,

        "courses": courses,

        "contributors": contributors,

        "top_students": top_students,

    }

    return render(
        request,
        "codexio_main/dashboard/dashboard.html",
        context
    )


def signup(request):

    if request.method == "POST":

        # LOGIN
        if "login_submit" in request.POST:

            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:

                if not user.is_verified:

                    messages.error(
                        request,
                        "Please verify your email first."
                    )

                    return redirect("/signup")

                login(request, user)

                if user.is_staff or user.is_superuser:
                    return redirect("courses:admin_dashboard")

                return redirect("/student_portal")

            else:

                messages.error(
                    request,
                    "Invalid username or password"
                )


        # REGISTER
        if "signup_submit" in request.POST:

            username = request.POST.get("username", "").strip()
            email = request.POST.get("email", "").strip()
            phone = request.POST.get("phone", "").strip()
            country = request.POST.get("country", "").strip()
            password = request.POST.get("password", "").strip()
            fullname = request.POST.get("fullname", "").strip()

            if User.objects.filter(username=username).exists():
                messages.error(request,"User already exists")
                return redirect("login_submit")

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return redirect("login_submit")

            if not all([
                username,
                email,
                phone,
                country,
                password,
                fullname
            ]):

               messages.error(
                  request,
                  "All fields are required."
               )

            else:

                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    phone=phone,
                    country=country,
                    fullname=fullname,
                    is_active=True
                )

                verification = EmailVerification.objects.create(
                   user=user
                )

                verification_link = request.build_absolute_uri(
                f"/verify-email/{verification.token}/"
                )

                subject = "Verify Your Email • CodexMingle community"

                html_content = render_to_string(
                    "codexio_main/emails/verify_email.html",
                    {
                       "user": user,
                       "verification_link": verification_link
                    }
                )

                text_content = strip_tags(html_content)

                email_message = EmailMultiAlternatives(
                   subject,
                   text_content,
                   settings.DEFAULT_FROM_EMAIL,
                   [user.email]
                )

                email_message.attach_alternative(html_content, "text/html")

                email_message.send()

                messages.success(
                   request,
                   "Account created successfully. Check your email to verify. If you do not see it in your regular mails, please check your spam folders."
                )

                return redirect("/signup")

    return render(request, "codexio_main/signupform.html")

def verify_email(request, token):

    verification = get_object_or_404(
        EmailVerification,
        token=token
    )

    verification.verified = True
    verification.save()

    user = verification.user

    user.is_verified = True

    user.verified_at = now()

    user.save()

    messages.success(
        request,
        "Email verified successfully."
    )

    return redirect("/signup")

def login_view(request):

    if request.method == "POST" and "login_submit" in request.POST:

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("/student_portal")

    return render(request, "codexio_main/signupform.html")

@login_required
def enrolled_courses(request):

    enrollments = Enrollment.objects.filter(user=request.user)

    return render(request, "codexio_main/dashboard/enrolled_courses.html", {
        "enrollments": enrollments
    })

@staff_member_required
def admin_dashboard(request):

    query = request.GET.get("q")

    users = User.objects.all()
    courses = Course.objects.all()

    modules = Module.objects.select_related('course').all()

    if query:
        users = User.objects.filter(username__icontains=query)
        courses = Course.objects.filter(title__icontains=query)

    context = {
        "users": users,
        "courses": courses,
        "modules": modules,
        "query": query
    }

    return render(request, "codexio_main/dashboard/admin_panel/admin.html", context)

@staff_member_required
def create_course(request):

    if request.method == "POST":

        topic = request.POST.get("topic")
        description = request.POST.get("description")
        course_type = request.POST.get("course_type")
        payment_type = request.POST.get("payment_type")
        price = request.POST.get("price")

        Course.objects.create(
            title=topic,
            description=description,
            course_type=course_type,
            payment_type=payment_type,
            price=price
        )

    return redirect('courses:admin_dashboard')

@staff_member_required
def enroll_user(request):


    if request.method == "POST":

        user_id = request.POST.get("user_id")
        course_id = request.POST.get("course_id")

        user = User.objects.get(id=user_id)
        course = Course.objects.get(id=course_id)

        if Enrollment.objects.filter(user=user, course=course).exists():
            messages.warning(request, "User already enrolled in this course.")

        else:
            Enrollment.objects.create(
                user=user,
                course=course
            )

            messages.success(request, "User successfully enrolled.")

    return redirect('courses:admin_dashboard')

@staff_member_required
def send_update(request):

    if request.method == "POST":

        message = request.POST.get("message")
        user_id = request.POST.get("user")

        if user_id == "all":

            UpdateNotification.objects.create(
                message=message
            )

        else:

            user = User.objects.get(id=user_id)

            UpdateNotification.objects.create(
                user=user,
                message=message
            )

    return redirect('courses:admin_dashboard')

@staff_member_required
def remove_user(request, user_id):

    user = User.objects.get(id=user_id)
    user.delete()

    return redirect('courses:admin_dashboard')

@staff_member_required
def create_module(request):

    if request.method == "POST":

        course_id = request.POST.get("course_id")
        title = request.POST.get("title")

        course = Course.objects.get(id=course_id)

        last_module = Module.objects.filter(course=course).order_by("-order").first()

        if last_module:
            order = last_module.order + 1
        else:
            order = 1

        Module.objects.create(
            course=course,
            title=title,
            order=order
        )

    return redirect("courses:admin_dashboard")

@staff_member_required
def create_assignment(request):

    if request.method == "POST":

        module_id = request.POST.get("module_id")
        title = request.POST.get("title")
        instructions = request.POST.get("instructions")

        if not module_id:
            return redirect("courses:admin_dashboard")

        module = get_object_or_404(Module, id=module_id)

        Assignment.objects.create(
            module=module,
            title=title,
            description=instructions
        )

    return redirect("courses:admin_dashboard")

@login_required
def live_courses(request):

    now = timezone.now()

    # upcoming cohorts (enrollment not yet open)
    upcoming_courses = Course.objects.filter(
        course_type="live",
        enrollment_open__gt=now
    )

    # cohorts where enrollment is open
    open_courses = Course.objects.filter(
        course_type="live",
        enrollment_open__lte=now
    )

    # courses the student enrolled in
    enrolled_courses = Course.objects.filter(
        enrollment__user=request.user,
        course_type="live"
    )

    context = {
        "upcoming_courses": upcoming_courses,
        "open_courses": open_courses,
        "enrolled_courses": enrolled_courses,
        "now": now
    }

    return render(request, "codexio_main/live_courses.html", context)

@login_required
def project_showcase(request):

    url = "https://api.github.com/users/codexmingleteam-sudo/repos"
    response = requests.get(url)

    projects = response.json()

    context = {
        "projects": projects
    }

    return render(request, "codexio_main/dashboard/projects.html", context)
