from django.urls import path
from .views import *

urlpatterns = [

    path(
        "recruit/",
        recruit_home,
        name="recruit_home"
    ),

    path(
        "student/<str:username>/",
        talent_detail,
        name="talent_detail"
    ),

    path("book-call/", book_call, name="book_call"),

    path("toggle/<int:user_id>/", toggle_student, name="toggle_student"),

]