from rest_framework import generics

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer
)


class BorrowingListView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

class UserBorrowingsListView(generics.ListAPIView):
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        user = self.request.user
        return Borrowing.objects.filter(user=user)
