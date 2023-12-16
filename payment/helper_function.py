import os

from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import stripe

from dotenv import load_dotenv

from .models import Borrowing, Payment


load_dotenv()
stripe_api_key = os.getenv("STRIPE_API_KEY")
CURRENCY = 100


@csrf_exempt
@api_view(["POST"])
def create_checkout_session(request, borrowing_id, total_amount=None):
    borrowing = Borrowing.objects.get(id=borrowing_id)

    if total_amount is None:
        borrowed_days = (borrowing.expected_return_date - borrowing.borrow_date).days
        total_price = borrowing.book_id.daily_fee * borrowed_days
        total_amount = int(total_price * CURRENCY)

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
        success_url="http://localhost:8000/success",
        cancel_url="http://localhost:8000/cancel",
    )

    payment = Payment.objects.create(
        status="b",
        type="p",
        session_url=session.url,
        session_id=session.id,
        borrowing=borrowing,
    )

    return HttpResponseRedirect(session.url, status=303)
