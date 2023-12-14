from rest_framework import generics

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
)


class BorrowingListView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.select_related("book", "user")
    serializer_class = BorrowingListSerializer


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.select_related("book", "user")
    serializer_class = BorrowingDetailSerializer
