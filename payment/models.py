from django.db import models
from django.utils import timezone

from borrowing.models import Borrowing


class Payment(models.Model):
    STATUS_CHOICES = [("b", "PENDING"), ("g", "PAID")]
    TYPE_CHOICES = [("p", "PAYMENT"), ("f", "FINE")]

    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    borrowing_id = models.ForeignKey(
        Borrowing, on_delete=models.CASCADE, related_name="payments"
    )
    session_url = models.URLField(max_length=200)
    session_id = models.CharField(max_length=100)

    @property
    def money_to_pay(self):
        if self.borrowing_id.actual_return_date:
            days_borrowed = (
                self.borrowing_id.actual_return_date
                - self.borrowing_id.borrow_date
            ).days
        else:
            days_borrowed = (timezone.now().date()
                             - self.borrowing_id.borrow_date).days

        return self.borrowing_id.book_id.daily_fee * days_borrowed
