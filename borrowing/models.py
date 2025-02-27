from django.db import models
from django.core.exceptions import ValidationError


class Borrowing(models.Model):
    """A model for borrowing"""
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="borrowings")
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="borrowings")
