from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import authenticate, login
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def signup_login_view(request):

    if request.method == "POST":

        # LOGIN
        if "login_submit" in request.POST:

            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("student_portal")
            else:
                messages.error(request, "Invalid username or password")


        # REGISTER
        if "signup_submit" in request.POST:

            username = request.POST.get("username")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            country = request.POST.get("country")
            password = request.POST.get("password")

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                phone=phone,
                country=country
            )

            login(request, user)

            return redirect("student_portal")

    return render(request, "codexio_main/signupform.html")

@login_required
def edit_profile(request):

    user = request.user

    if request.method == "POST":

        user.username = request.POST.get("username")
        user.phone = request.POST.get("phone")

        if request.FILES.get("profile_image"):
            user.profile_image = request.FILES.get("profile_image")

        user.save()

        return redirect("student_portal")

    return render(request,"users/edit_profile.html")

@login_required
def delete_account(request):

    if request.method == "POST":

        user = request.user
        user.delete()

        return redirect("home")

    return render(request,"users/delete_confirm.html")