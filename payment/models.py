from django.db import models
from django.utils import timezone

from borrowing.models import Borrowing


class Payment(models.Model):
    STATUS_CHOICES = [('PENDING', 'b'), ('PAID', 'g')]
    TYPE_CHOICES = [('PAYMENT', 'p'), ('FINE', 'f')]

    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE, related_name='payments')
    session_url = models.URLField(max_length=200)
    session_id = models.CharField(max_length=100)

    @property
    def money_to_pay(self):

        if self.borrowing.actual_return_date:
            days_borrowed = (self.borrowing.actual_return_date - self.borrowing.borrow_date).days
        else:
            days_borrowed = (timezone.now().date() - self.borrowing.borrow_date).days

        return self.borrowing.book.daily_fee * days_borrowed
