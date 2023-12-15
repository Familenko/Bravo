from rest_framework import serializers
from borrowing.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        ]

    def create(self, validated_data):
        book = validated_data["book"]
        user = self.context["request"].user

        if not user.is_authenticated:
            raise serializers.ValidationError(
                "User must be authenticated to borrow a book."
            )

        if book.inventory == 0:
            raise serializers.ValidationError("Book is out of stock.")

        borrowing = Borrowing.objects.create(
            expected_return_date=validated_data["expected_return_date"],
            actual_return_date=validated_data["actual_return_date"],
            book_id=book,
            user_id=user,
        )

        book.inventory -= 1
        book.save()

        return borrowing


class BorrowingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
        )
