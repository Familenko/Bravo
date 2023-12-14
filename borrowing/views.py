from django.shortcuts import render
from django.utils import timezone

from rest_framework import generics, status
from rest_framework import viewsets, mixins
from rest_framework.response import Response

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
)


class BorrowingViewSet():
    pass


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

        borrowing.book_id.inventory += 1
        borrowing.book_id.save()

        return Response(
            BorrowingSerializer(borrowing).data,
            status=status.HTTP_200_OK
        )
