from rest_framework import generics

from book.models import Book
from book.serializers import (
    BookSerializer,
)


class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = self.queryset
        title = self.request.query_params.get("title", None)
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset
