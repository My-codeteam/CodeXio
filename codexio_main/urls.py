from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('signup', views.signup, name='signup'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('about', views.about, name='about'),
    path('coming_soon', views.coming_soon, name='coming_soon'),
    path('student_portal', views.student_portal, name='student_portal'),
]