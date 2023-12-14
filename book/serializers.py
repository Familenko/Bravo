from rest_framework import serializers

from book.models import Book


class BookSerializer(serializers.ModelSerializer):
    pass


class BookListSerializer(serializers.ModelSerializer):
    pass


class BookDetailSerializer(serializers.ModelSerializer):
    pass
