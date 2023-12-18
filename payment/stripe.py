from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import stripe

import os
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_API_KEY")


@csrf_exempt
def create_checkout_test_session(request):
    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "Book4",
                    },
                    "unit_amount": 3000,
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="http://localhost:8000/success",
        cancel_url="http://localhost:8000/cancel",
    )

    return HttpResponseRedirect(session.url, status=303)
