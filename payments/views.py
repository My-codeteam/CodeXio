from django.shortcuts import render, redirect
import os
import requests
from courses.models import Course, Enrollment
from django.shortcuts import get_object_or_404
from .flutterwave import initialize_payment

def initiate_payment(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    amount = course.price
    email = request.user.email

    if course.price == 0:

        Enrollment.objects.create(
            user=request.user,
            course=course,
            paid=True
        )

        return redirect("course_modules",id=course.id)


    payload = {
        "tx_ref": f"course_{course.id}_user_{request.user.id}",
        "amount": str(amount),
        "currency": "NGN",
        "redirect_url": "http://127.0.0.1:8000/payment/verify/",
        "customer": {
            "email": email
        }
    }


    res = initialize_payment(payload)

        # safety check
    if res.get("status") != "success":
        return render(request, "payments/payment_error.html", {
                "error": res
        })

    return redirect(res["data"]["link"])

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
