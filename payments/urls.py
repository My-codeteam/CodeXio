from django.urls import path
from . import views


urlpatterns = [
    path("initiate/<int:course_id>/", views.initiate_payment, name="initiate_payment"),
]