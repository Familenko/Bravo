# myapp/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe

stripe.api_key = "sk_test_51ONXeYFz9k4dxDJnt41KauA0CrSAS0XOvygGQEdnhazhRxLWQtGGHxWFDWuBpDCJSsq8A0hXzNqN7uPqZY4puBrk00mxJcinIW"

@csrf_exempt
def create_checkout_session(request):
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'T-shirt',
                },
                'unit_amount': 2000,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/success',
        cancel_url='http://localhost:8000/cancel',
    )

    return redirect(session.url)
