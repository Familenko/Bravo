# from django.shortcuts import render

from rest_framework import generics, permissions

from borrowing.models import Borrowing
from payment.serializers import (
    PaymentDetailSerializer,
    PaymentListSerializer,
)

from .models import Payment


class PaymentList(
    generics.ListAPIView,
    generics.GenericAPIView
):
    queryset = Payment.objects.select_related("borrowing_id")
    serializer_class = PaymentListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        borrowings = Borrowing.objects.filter(user_id=self.request.user)
        payments = Payment.objects.filter(borrowing_id__in=borrowings)

        return payments


class PaymentDetail(
    generics.RetrieveAPIView,
    generics.GenericAPIView
):
    queryset = Payment.objects.all()
    serializer_class = PaymentDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        borrowings = Borrowing.objects.filter(user_id=self.request.user)
        payments = Payment.objects.filter(borrowing_id__in=borrowings, id=self.kwargs["pk"])
        return payments
