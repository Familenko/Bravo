from django.core.exceptions import ValidationError
from django.db import models

from book.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    def clean(self):
        if self.borrow_date > self.expected_return_date:
            raise ValidationError(
                "Expected return date should be after the borrow date."
            )

        if self.actual_return_date and self.actual_return_date > self.expected_return_date:
            raise ValidationError(
                "Actual return date should not be after the expected return date."
            )

    def save(self, *args, **kwargs):
        if self.actual_return_date and self.actual_return_date < self.borrow_date:
            raise ValidationError(
                "Actual return date should not be before the borrow date."
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Borrowed book {self.book_id} by user {self.user_id}"
