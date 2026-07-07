from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = "users"

urlpatterns = [
    path("signup_login/", views.signup_login_view, name="signup_login"),
    path("login/", views.signup_login_view, name="login"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("account/delete/", views.delete_account, name="delete_account"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("password-reset/request/", views.password_reset_request, name="password_reset_request"),
    path("password-reset/verify/", views.password_reset_verify, name="password_reset_verify"),
    path("password-reset/confirm/", views.password_reset_confirm, name="password_reset_confirm"),
]