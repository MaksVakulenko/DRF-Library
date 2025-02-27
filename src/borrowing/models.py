import datetime

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

from book.models import Book


class Borrowing(models.Model):
    """A model for borrowing"""
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrowings")

    @staticmethod
    def validate_if_user_has_borrowing(user_id: int):
        if Borrowing.objects.filter(user_id=user_id, actual_return_date__isnull=True).exists():
            raise ValidationError(
                {
                    "user": "You already have an active borrowing!"
                }
            )

    @staticmethod
    def validate_book_inventory(book: Book) -> None:
        if book.inventory <= 0:
            raise ValidationError(
                {
                    "book": f"The book {book.title} is out of stock!"
                }
            )

    @staticmethod
    def validate_expected_return_date(expected_date: datetime.date, borrow_date: datetime.date):
        today = datetime.date.today()
        if expected_date < today:
            raise ValidationError(
                {
                    "expected_return_date": "Expected return date can't be in the past!"
                }
            )

        if expected_date <= borrow_date:
            raise ValidationError(
                {
                    "expected_return_date": "Expected return date must be later than the borrow date!"
                }
            )

    def clean(self):
        Borrowing.validate_book_inventory(self.book)
        Borrowing.validate_expected_return_date(self.expected_return_date, self.borrow_date)
        Borrowing.validate_if_user_has_borrowing(self.user_id)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
