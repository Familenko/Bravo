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


class BorrowingDetailView(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,  # Додаємо ListModelMixin
    generics.GenericAPIView,
):
    queryset = Borrowing.objects.select_related("book_id", "user_id")
    serializer_class = BorrowingDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        user_id = self.request.query_params.get('user_id')
        is_active = self.request.query_params.get('is_active')

        if user.is_superuser:
            queryset = Borrowing.objects.all()

            if user_id:
                queryset = queryset.filter(user_id=user_id)

            if is_active:
                is_active = is_active.lower() == 'true'
                queryset = queryset.filter(is_active=is_active)

        else:
            queryset = Borrowing.objects.filter(user_id=user.id)

        return queryset

    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)


class BorrowingReturnView(generics.UpdateAPIView):
    queryset = Borrowing.objects.select_related("book_id", "user_id")
    serializer_class = BorrowingSerializer

    def update(self, request, *args, **kwargs):
        borrowing = self.get_object()

        if borrowing.actual_return_date is not None:
            return Response(
                {"message": "Book already returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        borrowing.actual_return_date = timezone.now()

        overdue_days = (borrowing.actual_return_date - borrowing.expected_return_date).days

        if overdue_days > 0:
            daily_fee = borrowing.book_id.daily_fee
            fine_amount = overdue_days * daily_fee * FINE_MULTIPLIER

            create_checkout_session(self.request, borrowing.id, fine_amount)

        else:
            create_checkout_session(self.request, borrowing.id)

        borrowing.book_id.inventory += 1
        borrowing.book_id.save()

        return Response(BorrowingSerializer(borrowing).data, status=status.HTTP_200_OK)


class BorrowingCreateView(generics.CreateAPIView):
    queryset = Borrowing.objects.select_related("book_id", "user_id")
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        borrowing = serializer.save()

        create_checkout_session(self.request, borrowing.id)

        return Response(serializer.data)
