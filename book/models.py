from django.db import models


class Book(models.Model):
    COVER_TYPES = (
        ("HARD", "Hard"),
        ("SOFT", "Soft"),
    )
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(choices=COVER_TYPES)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_length=6, decimal_places=2)

    def __str__(self):
        return f"{self.title} by {self.author}"
