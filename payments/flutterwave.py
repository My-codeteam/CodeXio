import requests
import os

FLW_SECRET_KEY = os.getenv("FLW_SECRET_KEY")


def initialize_payment(payload):
    url = "https://api.flutterwave.com/v3/payments"

    headers = {
        "Authorization": f"Bearer {FLW_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()