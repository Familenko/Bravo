from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, reverse
from rest_framework.decorators import api_view
import stripe
from dotenv import load_dotenv
import os

from .models import Borrowing, Payment

load_dotenv()
stripe_api_key = os.getenv("STRIPE_API_KEY")
CURRENCY = 100


@csrf_exempt
@api_view(["POST"])
def create_checkout_session(request, borrowing_id, total_amount=None):
    borrowing = get_object_or_404(Borrowing, id=borrowing_id)

    type_choices = "f"
    status_choices = "b"

    if total_amount is None:
        borrowed_days = (borrowing.expected_return_date - borrowing.borrow_date).days
        total_price = borrowing.book_id.daily_fee * borrowed_days
        total_amount = int(total_price * CURRENCY)

        type_choices = "p"

    session = stripe.checkout.Session.create(
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": f"Book - {borrowing.book_id.title}",
                },
                "unit_amount": total_amount,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=request.build_absolute_uri(
            reverse(
                'payment:success', kwargs={'borrowing_id': borrowing_id}
            )
        ),
        cancel_url=request.build_absolute_uri(
            reverse(
                'payment:cancel', kwargs={'borrowing_id': borrowing_id}
            )
        ),
    )

    payment = Payment.objects.create(
        status=status_choices,
        type=type_choices,
        session_url=session.url,
        session_id=session.id,
        borrowing_id=borrowing,
    )

    return HttpResponseRedirect(session.url, status=303)
