from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = "users"

urlpatterns = [

path("profile/edit/", views.edit_profile, name="edit_profile"),
path("account/delete/", views.delete_account, name="delete_account"),
path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
]