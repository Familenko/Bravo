from django.urls import path

from payment.stripe import create_checkout_session
from payment.views import PaymentList, PaymentDetail

urlpatterns = [
    path("stripe/", create_checkout_session, name="stripe"),
    path("list/", PaymentList.as_view(), name="list"),
    path(
        "detail/<int:pk>/",
        PaymentDetail.as_view(),
        name="detail",
    ),
]

app_name = "payment"
