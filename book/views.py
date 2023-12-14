from django.shortcuts import render

from rest_framework import viewsets, mixins

from book.models import Book
from book.serializers import (
    BookSerializer,
    BookListSerializer,
    BookDetailSerializer,
)


class BookViewSet():
    pass
