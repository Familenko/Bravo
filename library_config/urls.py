from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "api/book/",
        include("book.urls",
                namespace="book")),

    path(
        "api/borrowing/",
        include("borrowing.urls",
                namespace="borrowing")),

    path(
        "api/payment/",
        include("payment.urls",
                namespace="payment")),

    path(
        "api/user/",
        include("user.urls",
                namespace="user")),
]
