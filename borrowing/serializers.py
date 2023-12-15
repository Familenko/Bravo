from rest_framework import serializers
from book.serializers import BookSerializer
from borrowing.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user_id",
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
            book=book,
            user=user,
        )

        book.inventory -= 1
        book.save()

        return borrowing

    def create(self, validated_data):
        book = validated_data["book"]
        user = self.context["request"].user



        if not user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated to borrow a book.")

        if book.inventory == 0:
            raise serializers.ValidationError("Book is out of stock.")

        borrowing = Borrowing.objects.create(
            expected_return_date=validated_data["expected_return_date"],
            actual_return_date=validated_data["actual_return_date"],
            book=book,
            user=user
        )

        book.inventory -= 1
        book.save()

        return borrowing


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
            "book",
        )
