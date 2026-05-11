from django.shortcuts import render

import requests
from django.shortcuts import redirect
from courses.models import Course, Enrollment

def initiate_payment(request):

    if request.method == "POST":

        amount = request.POST['amount']
        email = request.POST['email']
        course_id = request.POST['course_id']

        course = Course.objects.get(id=course_id)

        if course.price == 0:

            Enrollment.objects.create(
                user=request.user,
                course=course,
                paid=True
            )

            return redirect("course_modules",id=course.id)

        url = "https://api.flutterwave.com/v3/payments"

        payload = {
            "tx_ref": "course_payment",
            "amount": amount,
            "currency": "NGN",
            "redirect_url": "http://127.0.0.1:8000/payment/verify/",
            "customer": {
                "email": email
            }
        }

        headers = {
            "Authorization": "Bearer FLW_SECRET_KEY"
        }

        response = requests.post(url,json=payload,headers=headers)

        payment_link = response.json()['data']['link']

        return redirect(payment_link)
# Create your views here.
