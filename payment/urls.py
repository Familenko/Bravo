from django.urls import path

from payment.stripe import create_checkout_test_session
from payment.views import PaymentList, PaymentDetail, SuccessView, CancelView

urlpatterns = [
    path("stripe/", create_checkout_test_session, name="stripe"),
    path("list/", PaymentList.as_view(), name="list"),
    path(
        "detail/<int:pk>/",
        PaymentDetail.as_view(),
        name="detail",
    ),
    path("success/<int:borrowing_id>/", SuccessView.as_view(), name="success"),
    path("cancel/<int:borrowing_id>/", CancelView.as_view(), name="cancel"),
]

app_name = "payment"
