from rest_framework import serializers

from book.models import Book
from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "type",
            "borrowing",
            "session_url",
            "session_id",
        )


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Payment


class BorrowedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("daily_fee", "title")


class PaymentDetailSerializer(serializers.ModelSerializer):
    taken_book = BorrowedBookSerializer(
        source="borrowing_id.book_id", read_only=True
    )

    class Meta:
        fields = (
            "id",
            "status",
            "type",
            "borrowing_id",
            "session_url",
            "session_id",
            "taken_book",
        )

        model = Payment


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "status",
            "type",
            "borrowing_id",
            "session_url",
            "session_id",
        )

    def validate(self, attrs):
        borrowing_id = attrs.get("borrowing_id")
        if borrowing_id.actual_return_date:
            raise serializers.ValidationError(
                "You can't pay for already returned book"
            )
        return attrs
