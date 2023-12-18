from django.utils import timezone

from rest_framework import generics, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
)
from payment.helper_function import create_checkout_session

FINE_MULTIPLIER = 2


class BorrowingListView(
    mixins.ListModelMixin,
    generics.GenericAPIView,
):
    queryset = Borrowing.objects.select_related("book_id", "user_id")
    serializer_class = BorrowingDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        user_id = self.request.query_params.get("user_id", None)
        is_active = self.request.query_params.get("is_active", None)

        if user.is_superuser:
            queryset = Borrowing.objects.all()

            if user_id:
                queryset = queryset.filter(user_id=user_id)

            if is_active is not None:
                is_active = bool(is_active and is_active.lower() == "true")
                queryset = queryset.filter(is_active=is_active)

        else:
            queryset = Borrowing.objects.filter(user_id=user.id)

        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.select_related("book_id", "user_id")
    serializer_class = BorrowingDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = Borrowing.objects.all()
        else:
            queryset = Borrowing.objects.filter(user_id=user.id)

        return queryset.filter(id=self.kwargs["pk"])


class BorrowingReturnView(generics.UpdateAPIView):
    queryset = Borrowing.objects.select_related("book_id", "user_id")
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        borrowing = self.get_object()

        if borrowing.actual_return_date is not None:
            return Response(
                {"message": "Book already returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        borrowing.actual_return_date = timezone.now().date()

        overdue_days = (borrowing.actual_return_date - borrowing.expected_return_date).days

        if overdue_days > 0:
            daily_fee = borrowing.book_id.daily_fee
            fine_amount = overdue_days * daily_fee * FINE_MULTIPLIER

            create_checkout_session(self.request, borrowing.id, fine_amount)

        borrowing.book_id.inventory += 1
        borrowing.book_id.save()
        borrowing.save()

        return Response(BorrowingSerializer(borrowing).data, status=status.HTTP_200_OK)


class BorrowingCreateView(generics.CreateAPIView):
    queryset = Borrowing.objects.select_related("book_id", "user_id")
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def perform_create(self, serializer):
        borrowing = serializer.save()

        http_request = self.request._request

        create_checkout_session(http_request, borrowing.id)

        return Response(serializer.data)
