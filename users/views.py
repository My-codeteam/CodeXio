from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User, PasswordReset
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now, timedelta
from services.resend_service import send_email
import random
import string

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


def password_reset_request(request):
    """Request password reset by email"""

    if request.method == "POST":
        email = request.POST.get("email", "").strip()

        try:
            user = User.objects.get(email=email)

            # Generate 6-digit verification code
            code = ''.join(random.choices(string.digits, k=6))

            # Delete old reset requests
            PasswordReset.objects.filter(user=user, is_used=False).delete()

            # Create new password reset request
            reset = PasswordReset.objects.create(
                user=user,
                code=code,
                expires_at=now() + timedelta(minutes=15)
            )

            # Send verification code via email
            html_content = f"""
            <html>
                <body>
                    <h2>Password Reset Request</h2>
                    <p>Hi {user.username},</p>
                    <p>We received a request to reset your password. Use the verification code below:</p>
                    <h3 style="color: #007bff; font-family: monospace; letter-spacing: 5px;">{code}</h3>
                    <p>This code will expire in 15 minutes.</p>
                    <p>If you didn't request this, please ignore this email.</p>
                    <p>Best regards,<br>CodeXio Team</p>
                </body>
            </html>
            """

            send_email(
                subject="Password Reset Verification Code",
                recipient=user.email,
                html_content=html_content
            )

            messages.success(request, "Verification code sent to your email!")
            return redirect("users:password_reset_verify")

        except User.DoesNotExist:
            messages.error(request, "Email not found in our system")

    return render(request, "users/password_reset_request.html")


def password_reset_verify(request):
    """Verify the reset code"""

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        code = request.POST.get("code", "").strip()

        try:
            user = User.objects.get(email=email)
            reset = PasswordReset.objects.filter(
                user=user,
                code=code,
                is_used=False
            ).first()

            if not reset:
                messages.error(request, "Invalid verification code")
                return render(request, "users/password_reset_verify.html")

            if not reset.is_valid():
                messages.error(request, "Verification code has expired. Please try again.")
                return redirect("users:password_reset_request")

            # Code is valid, proceed to password reset
            request.session['reset_user_id'] = user.id
            request.session['reset_code_id'] = reset.id
            messages.success(request, "Code verified! Please set your new password.")
            return redirect("users:password_reset_confirm")

        except User.DoesNotExist:
            messages.error(request, "Email not found")

    return render(request, "users/password_reset_verify.html")


def password_reset_confirm(request):
    """Set the new password"""

    if request.method == "POST":
        user_id = request.session.get('reset_user_id')
        reset_code_id = request.session.get('reset_code_id')
        new_password = request.POST.get("new_password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not user_id or not reset_code_id:
            messages.error(request, "Session expired. Please start over.")
            return redirect("users:password_reset_request")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "users/password_reset_confirm.html")

        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters long")
            return render(request, "users/password_reset_confirm.html")

        try:
            user = User.objects.get(id=user_id)
            reset = PasswordReset.objects.get(id=reset_code_id)

            if reset.is_used or not reset.is_valid():
                messages.error(request, "This reset request is no longer valid")
                return redirect("users:password_reset_request")

            # Update password
            user.set_password(new_password)
            user.save()

            # Mark code as used
            reset.is_used = True
            reset.save()

            # Clear session
            if 'reset_user_id' in request.session:
                del request.session['reset_user_id']
            if 'reset_code_id' in request.session:
                del request.session['reset_code_id']

            messages.success(request, "Password reset successfully! Please login with your new password.")
            return redirect("users:login")

        except (User.DoesNotExist, PasswordReset.DoesNotExist):
            messages.error(request, "An error occurred. Please try again.")
            return redirect("users:password_reset_request")

    return render(request, "users/password_reset_confirm.html")


@login_required
def edit_profile(request):

    user = request.user

    if request.method == "POST":

        user.fullname = request.POST.get("fullname")
        user.phone = request.POST.get("phone")

        if request.FILES.get("profile_image"):
            user.profile_image = request.FILES.get("profile_image")

        user.save()

        return redirect("/student_portal")

    return render(request,"users/edit_profile.html")

@login_required
def delete_account(request):

    if request.method == "POST":

        user = request.user
        user.delete()

        return redirect("home")

    return render(request,"users/delete_confirm.html")