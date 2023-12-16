from rest_framework import generics

from book.models import Book
from book.serializers import (
    BookSerializer,
)


class BookListView(generics.ListCreateAPIView):
    # for some reason queryset in here don't let to call it as self.queryset in def get_queryset
    serializer_class = BookSerializer

    def get_queryset(self):
        title = self.request.query_params.get("title")
        queryset = Book.objects.all()
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
