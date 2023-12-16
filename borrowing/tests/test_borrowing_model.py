from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.test import TestCase
from borrowing.models import Borrowing
from book.models import Book


class BorrowingModelTests(TestCase):
    def test_create_borrowing(self):
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=10.00,
        )

        user = get_user_model().objects.create_user(
            email="test@example.com", password="testpassword"
        )

        borrowing = Borrowing(
            borrow_date=datetime.now().date(),
            expected_return_date=(datetime.now() + timedelta(days=1)).date(),
            actual_return_date=(datetime.now() + timedelta(days=2)).date(),
            book_id=book,
            user_id=user,
        )
        borrowing.save()

        saved_borrowing = Borrowing.objects.get(pk=borrowing.pk)

        self.assertEqual(saved_borrowing.borrow_date, datetime.now().date())
        self.assertEqual(
            saved_borrowing.expected_return_date,
            (datetime.now() + timedelta(days=1)).date(),
        )
        self.assertEqual(
            saved_borrowing.actual_return_date,
            (datetime.now() + timedelta(days=2)).date(),
        )
        self.assertEqual(saved_borrowing.book_id, book)
        self.assertEqual(saved_borrowing.user_id, user)

        self.assertIsNotNone(saved_borrowing.borrow_date)


class BookModelTests(TestCase):
    def test_create_book(self):
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=10.00,
        )

        saved_book = Book.objects.get(pk=book.pk)

        self.assertEqual(saved_book.title, "Test Book")
        self.assertEqual(saved_book.author, "Test Author")
        self.assertEqual(saved_book.cover, "HARD")
        self.assertEqual(saved_book.inventory, 10)
        self.assertEqual(saved_book.daily_fee, 10.00)

        self.assertIsNotNone(saved_book.id)

    def test_str_representation(self):
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=10.00,
        )

        self.assertEqual(str(book), "Test Book by Test Author")

    def test_update_book(self):
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=10.00,
        )

        book.title = "Updated Book Title"
        book.author = "Updated Book Author"
        book.cover = "SOFT"
        book.inventory = 5
        book.daily_fee = 15.00
        book.save()

        updated_book = Book.objects.get(pk=book.pk)
        self.assertEqual(updated_book.title, "Updated Book Title")
        self.assertEqual(updated_book.author, "Updated Book Author")
        self.assertEqual(updated_book.cover, "SOFT")
        self.assertEqual(updated_book.inventory, 5)
        self.assertEqual(updated_book.daily_fee, 15.00)

    def test_create_borrowing(self):
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=10.00,
        )

        user = get_user_model().objects.create_user(
            email="test@example.com", password="testpassword"
        )

        borrowing = Borrowing(
            borrow_date=datetime.now().date(),
            expected_return_date=(datetime.now() + timedelta(days=1)).date(),
            actual_return_date=(datetime.now() + timedelta(days=2)).date(),
            book_id=book,
            user_id=user,
        )
        borrowing.save()

        saved_borrowing = Borrowing.objects.get(pk=borrowing.pk)

        self.assertEqual(saved_borrowing.borrow_date, datetime.now().date())
        self.assertEqual(
            saved_borrowing.expected_return_date,
            (datetime.now() + timedelta(days=1)).date(),
        )
        self.assertEqual(
            saved_borrowing.actual_return_date,
            (datetime.now() + timedelta(days=2)).date(),
        )
        self.assertEqual(saved_borrowing.book_id, book)
        self.assertEqual(saved_borrowing.user_id, user)

        self.assertIsNotNone(saved_borrowing.borrow_date)

    def test_invalid_borrow_date(self):
        book = Book.objects.create(
            title="Invalid Borrowing Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=10.00,
        )

        user = get_user_model().objects.create_user(
            email="test@example.com", password="testpassword"
        )

        invalid_borrowing = Borrowing(
            borrow_date=datetime.now().date() + timedelta(days=2),
            expected_return_date=(datetime.now() + timedelta(days=1)).date(),
            book_id=book,
            user_id=user,
        )

        with self.assertRaises(ValidationError):
            invalid_borrowing.clean()

    def test_actual_return_date_after_expected_return_date(self):
        book = Book.objects.create(
            title="Invalid Return Date Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=10.00,
        )

        user = get_user_model().objects.create_user(
            email="test@example.com", password="testpassword"
        )

        invalid_borrowing = Borrowing(
            borrow_date=datetime.now().date(),
            expected_return_date=(datetime.now() + timedelta(days=1)).date(),
            actual_return_date=(datetime.now() + timedelta(days=2)).date(),
            book_id=book,
            user_id=user,
        )

        with self.assertRaises(ValidationError):
            invalid_borrowing.clean()
