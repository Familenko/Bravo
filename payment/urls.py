from django.urls import path, include
from rest_framework import routers

from payment.stripe import create_checkout_session

urlpatterns = [
    path("stripe/", create_checkout_session, name="stripe"),
]

app_name = "payment"
