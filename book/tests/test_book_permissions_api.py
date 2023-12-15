from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase

from book.models import Book
from book.serializers import BookSerializer

BOOK_LIST_URL = reverse("book:book-list")


def detail_url(book_id):
    return reverse("book:book-detail", args=[book_id])


def sample_book(**params):
    defaults = {
        "title": "testtitle",
        "author": "testauthor",
        "cover": "HARD",
        "inventory": 10,
        "daily_fee": 11.99,
    }
    defaults.update(**params)
    return Book.objects.create(**defaults)


class UnauthenticatedBookApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_books(self):
        sample_book()
        response = self.client.get(BOOK_LIST_URL)

        books = Book.objects.order_by("id")
        serializer = BookSerializer(books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_detail_book(self):
        book = sample_book()

        url = detail_url(book.id)
        response = self.client.get(url)

        serializer = BookSerializer(book)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_forbidden(self):
        payload = {
            "title": "testtitle",
            "author": "testauthor",
            "cover": "HARD",
            "inventory": 1,
            "daily_fee": 10,
        }
        response = self.client.post(BOOK_LIST_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@testmail.com", "testpassword"
        )
        self.client.force_authenticate(self.user)
        self.book = sample_book()
        self.url = detail_url(self.book.id)

    def test_create_forbidden(self):
        payload = {
            "title": "testtitle",
            "author": "testauthor",
            "cover": "HARD",
            "inventory": 1,
            "daily_fee": 10,
        }
        response = self.client.post(BOOK_LIST_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_forbidden(self):
        payload = {
            "title": "testtitle2",
            "author": "testauthor2",
            "cover": "HARD",
            "inventory": 1,
            "daily_fee": 10.00,
        }
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_forbidden(self):
        payload = {
            "title": "testtitle2",
            "author": "testauthor2",
        }
        response = self.client.patch(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_forbidden(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@testmail.com", "testpassword", is_staff=True
        )
        self.client.force_authenticate(self.user)
        self.book = sample_book()
        self.url = detail_url(self.book.id)

    def test_create_book(self):
        payload = {
            "title": "testtitle",
            "author": "testauthor",
            "cover": "HARD",
            "inventory": 1,
            "daily_fee": 10,
        }
        response = self.client.post(BOOK_LIST_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        book = Book.objects.get(id=response.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(book, key))

    def test_put_book(self):
        payload = {
            "title": "testtitle2",
            "author": "testauthor2",
            "cover": "HARD",
            "inventory": 1,
            "daily_fee": 10.00,
        }
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(self.book, key))

    def test_patch_book(self):
        payload = {
            "title": "testtitle2",
            "author": "testauthor2",
        }
        response = self.client.patch(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(self.book, key))

    def test_delete_book(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
