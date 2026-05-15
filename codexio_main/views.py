import nltk

from nltk.chat.util import Chat, reflections
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from users.models import User
from django.db.models.functions import Now
from datetime import timedelta
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model

User = get_user_model()
from courses.models import Course, Enrollment, UpdateNotification
from django.contrib.auth import authenticate, login
from django.contrib import messages


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
    return render(request, 'codexio_main/index.html')

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
    total_courses = Course.objects.count()

    total_members = User.objects.count()

    courses_enrolled = Enrollment.objects.filter(
        user=request.user
    ).count()

    courses = Course.objects.order_by('-id')[:6]

    updates = UpdateNotification.objects.all()

    # GitHub repos
    url = "https://api.github.com/orgs/CodexMingle/repos"

    response = requests.get(url)

    repos = response.json()

    total_repos = len(repos)

    context = {

        "total_courses": total_courses,

        "total_members": total_members,

        "courses_enrolled": courses_enrolled,

        "total_repos": total_repos,

        "updates": updates,

        "courses": courses

    }

    return render(request, 'codexio_main/dashboard/dashboard.html', context)


def signup(request):

    if request.method == "POST":

        # LOGIN
        if "login_submit" in request.POST:

            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user.is_superuser or user.is_staff:
                login(request, user)
                return redirect("courses:admin_dashboard")
            elif user is not None:
                login(request, user)
                return redirect("/student_portal")

            else:
                messages.error(request, "Invalid username or password")


        # REGISTER
        if "signup_submit" in request.POST:

            username = request.POST.get("username")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            country = request.POST.get("country")
            password = request.POST.get("password")

            if User.objects.filter(username=username).exists():
                messages.error(request,"Username already exists")
                return redirect("login_submit")

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                phone=phone,
                country=country
            )

            login(request, user)

            return redirect("/student_portal")

    return render(request, "codexio_main/signupform.html")


def login_view(request):

    if request.method == "POST" and "login_submit" in request.POST:

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("/student_portal")

    return render(request, "codexio_main/signupform.html")

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

    if query:
        users = User.objects.filter(username__icontains=query)
        courses = Course.objects.filter(topic__icontains=query)

    context = {
        "users": users,
        "courses": courses,
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

        Course.objects.create(
            title=topic,
            description=description,
            course_type=course_type,
            payment_type=payment_type
        )

    return redirect('courses:admin_dashboard')

@staff_member_required
def enroll_user(request):

    if request.method == "POST":

        user_id = request.POST.get("user_id")
        course_id = request.POST.get("course_id")

        user = User.objects.get(id=user_id)
        course = Course.objects.get(id=course_id)

        Enrollment.objects.create(
            student=user,
            course=course
        )

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
