from django.db import models
from django.core.exceptions import ValidationError


class Borrowing(models.Model):
    """A model for borrowing"""
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="borrowings")
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="borrowings")

    @staticmethod
    def validate_book_inventory(book: "Book") -> None:
        if book.inventory <= 0:
            raise ValidationError(
                {
                    "book": f"The book {book.title} is out of stock!"
                }
            )

    def clean(self):
        Borrowing.validate_book_inventory(self.book)

    def save(
        self,
        force_insert = ...,
        force_update = ...,
        using = ...,
        update_fields = ...,
    ):
        self.full_clean()
        self.save(force_insert, force_update, using, update_fields)
