from django.shortcuts import render, redirect
import os
import requests
from courses.models import Course, Enrollment
from django.shortcuts import get_object_or_404
from .lemonsqueezy import create_checkout
from .forms import PaymentProofForm

def initiate_payment(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":

        form = PaymentProofForm(request.POST, request.FILES)

        if form.is_valid():

            payment = form.save(commit=False)

            payment.user = request.user
            payment.course = course
            payment.amount = course.price

            payment.save()

            return render(request, "payments/payment_submitted.html")

    else:
        form = PaymentProofForm()

    return render(request, "payments/manual_payment.html", {
        "course": course,
        "form": form
    })

"""
def verify_payment(request):

    status = request.GET.get("status")
    tx_ref = request.GET.get("tx_ref")
    transaction_id = request.GET.get("transaction_id")

    if status != "successful":
        return render(request, "payments/payment_error.html", {
            "error": "Payment not successful"
        })

    url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"

    headers = {
        "Authorization": f"Bearer {os.getenv('FLW_SECRET_KEY')}"
    }

    response = requests.get(url, headers=headers)
    res = response.json()

    if res["status"] == "success":
        data = res["data"]

        # SECURITY CHECK
        if data["status"] == "successful":

            return render(request, "paymentspayment_success.html")

    return render(request, "payments/payment_error.html", {
        "error": res
    })

# Create your views here.
"""
