from django.urls import path
from . import views
# from .views import verify_payment

app_name = "payments"

urlpatterns = [
    path("initiate/<int:course_id>/", views.initiate_payment, name="initiate_payment"),
    # path("payment/verify/", verify_payment, name="verify_payment"),
]