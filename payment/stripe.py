from django.http import HttpResponse, HttpResponseRedirect
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
                    'name': 'Book3',
                },
                'unit_amount': 3000,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/success',
        cancel_url='http://localhost:8000/cancel',
    )

    return HttpResponseRedirect(session.url, status=303)
