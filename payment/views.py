# from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

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
        borrowings = Borrowing.objects.filter(user_id=self.request.user.pk)
        payments = Payment.objects.filter(borrowing_id__in=borrowings)

        return payments


class PaymentDetail(
    generics.RetrieveAPIView,
    generics.GenericAPIView
):
    queryset = Payment.objects.all()
    serializer_class = PaymentDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     borrowings = Borrowing.objects.filter(user_id=self.request.user)
    #     payments = Payment.objects.filter(borrowing_id__in=borrowings)
    #     return payments.filter(
    #         id=self.kwargs["pk"],
    #     )

    def get_queryset(self):
        borrowings = Borrowing.objects.filter(user_id=self.request.user)
        payments = Payment.objects.filter(borrowing_id__in=borrowings, id=self.kwargs["pk"])
        return payments


class SuccessView(APIView):
    def get(self, request, borrowing_id):
        payment = get_object_or_404(Payment, borrowing_id=borrowing_id)
        payment.status = Payment.STATUS_CHOICES.PAID
        payment.save()
        if payment.type == "f":
            return Response(
                {"message": "Your payment for fine was successful"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Your payment was successful"},
            status=status.HTTP_200_OK
        )


class CancelView(APIView):
    def get(self, request):
        return Response(
            {"message": "You can pay for it later (in 24 hours from now)"},
            status=status.HTTP_400_BAD_REQUEST
        )
