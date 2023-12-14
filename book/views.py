from rest_framework import generics

from book.models import Book
from book.serializers import (
    BookSerializer,
    BookListSerializer,
    BookDetailSerializer,
)


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
