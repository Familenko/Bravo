from django.shortcuts import render
from django.utils import timezone

from rest_framework import generics, status
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import generics

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
)


class BorrowingListView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.select_related("book", "user")
    serializer_class = BorrowingSerializer


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.select_related("book", "user")
    serializer_class = BorrowingSerializer


class UserBorrowingsListView(generics.ListAPIView):
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        user = self.request.user
        return Borrowing.objects.filter(user=user)


class BorrowingReturnView(generics.UpdateAPIView):
    queryset = Borrowing.objects.select_related('book', 'user')
    serializer_class = BorrowingSerializer

    def update(self, request, *args, **kwargs):
        borrowing = self.get_object()

        if borrowing.actual_return_date is not None:
            return Response(
                {'message': 'Book already returned.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        borrowing.actual_return_date = timezone.now()


        return Response(
            BorrowingSerializer(borrowing).data,
            status=status.HTTP_200_OK
        )
