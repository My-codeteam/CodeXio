import requests
import os

LEMON_API_KEY = os.getenv("LEMON_API_KEY")
STORE_ID = os.getenv("LEMON_STORE_ID")
VARIANT_ID = os.getenv("LEMON_VARIANT_ID")


def create_checkout(email, course):

    url = "https://api.lemonsqueezy.com/v1/checkouts"

    headers = {
        "Authorization": f"Bearer {LEMON_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "data": {
            "type": "checkouts",
            "attributes": {
                "checkout_data": {
                    "email": email,
                    "custom": {
                        "course_id": course.id
                    }
                }
            },
            "relationships": {
                "store": {
                    "data": {
                        "type": "stores",
                        "id": STORE_ID
                    }
                },
                "variant": {
                    "data": {
                        "type": "variants",
                        "id": VARIANT_ID
                    }
                }
            }
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()