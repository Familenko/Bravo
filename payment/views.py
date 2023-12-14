from django.shortcuts import render

from rest_framework import viewsets, mixins

from payment.models import Payment
from payment.serializers import (
    PaymentSerializer,
    PaymentDetailSerializer,
    PaymentCreateSerializer,
    PaymentListSerializer,
)


class PaymentViewSet():
    pass
