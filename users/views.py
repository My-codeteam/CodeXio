from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import authenticate, login
from .models import User

def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password=password)

        if user:
            login(request,user)
            return redirect("dashboard")

    return render(request,"auth/login.html")



def signup(request):

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        country = request.POST['country']
        password = request.POST['password']

        user = User.objects.create_user(
            username=username,
            email=email,
            phone=phone,
            country=country,
            password=password
        )

        return redirect("login")

    return render(request,"auth/signup.html")