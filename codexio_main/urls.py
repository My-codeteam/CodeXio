from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path('', views.home, name='index'),
    path('signup', views.signup, name='signup'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('about', views.about, name='about'),
    path('coming_soon', views.coming_soon, name='coming_soon'),
    path('student_portal', views.student_portal, name='student_portal'),
    path('enrolled_courses', views.enrolled_courses, name='enrolled_courses'),
    path('admin-dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('create-course/', views.create_course, name='create_course'),
    path('enroll-user/', views.enroll_user, name='enroll_user'),
    path('send-update/', views.send_update, name='send_update'),
    path('remove-user/<int:user_id>/', views.remove_user, name='remove_user'),
    path("create-module/", views.create_module, name="create_module"),
    path("create-assignment/", views.create_assignment, name="create_assignment"),
    path('live-cohorts/', views.live_courses, name='live_courses'),
    path('project-showcase/', views.project_showcase, name='project_showcase'),
    path(
    "verify-email/<uuid:token>/",
    views.verify_email,
    name="verify_email"),
    path(
    "feedback/",
    views.feedback,
    name="feedback"
    ),
    path('testimonial', views.testimonial, name='testimonial')
]