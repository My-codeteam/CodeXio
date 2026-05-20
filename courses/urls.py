from django.urls import path
from . import views


urlpatterns = [

    path("courses/", views.course_list, name="course_list"),

    path("course/<int:course_id>/",
         views.course_detail,
         name="course_detail"),

    path("module/<int:module_id>/",
         views.module_detail,
         name="module_detail"),

    path("enroll/<int:course_id>/", views.enroll_course, name="enroll_course"),

    path(
    "submit-assignment/<int:assignment_id>/",
    views.submit_assignment,
    name="submit_assignment"),

    path(
    "module/<int:module_id>/complete/",
    views.complete_module,
    name="complete_module"),

    path(
    "certificate/<int:completed_id>/",
    views.certificate_view,
    name="certificate_view"),

    path(
        "download/<str:certificate_id>/",
        views.download_certificate,
        name="download_certificate"
    ),

    path(
        "verify/<str:certificate_id>/",
        views.verify_certificate,
        name="verify_certificate"
    ),

    path(
        "my-certificates/",
        views.my_certificates,
        name="my_certificates"
    ),


]