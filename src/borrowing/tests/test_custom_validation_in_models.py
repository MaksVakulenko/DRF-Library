import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from borrowing.models import Borrowing
from borrowing.tests.base_setup import BaseSetUpForTest


class TestBorrowingValidations(TestCase):
    def setUp(self):
        self.base_setup = BaseSetUpForTest()
        self.base_setup.setUp()

    def test_user_cannot_borrow_if_has_expired_borrowing(self):
        """
        Ensure a user cannot borrow a book if they have an expired borrowing.
        """
        expired_borrowing = self.base_setup.expired_borrowing
        new_borrowing = Borrowing(
            user=expired_borrowing.user,
            book=self.base_setup.book_available,
            expected_return_date=datetime.date.today() + datetime.timedelta(days=5),
        )
        with self.assertRaises(ValidationError, msg="You have an expired borrowing!"):
            new_borrowing.clean()

    def test_user_cannot_borrow_if_has_pending_payment(self):
        """
        Ensure a user cannot borrow a book if they have a pending payment.
        """
        pending_payment = self.base_setup.pending_payment
        new_borrowing = Borrowing(
            user=pending_payment.borrowing.user,
            book=self.base_setup.book_available,
            expected_return_date=datetime.date.today() + datetime.timedelta(days=5),
        )
        with self.assertRaises(ValidationError, msg="You have a pending payment!"):
            new_borrowing.clean()

    def test_expected_return_date_cannot_be_today_or_past(self):
        """
        Ensure that expected return date cannot be today or in the past.
        """
        user = self.base_setup.user
        book = self.base_setup.book_available

        for invalid_date in [
            datetime.date.today(),
            datetime.date.today() - datetime.timedelta(days=1),
        ]:
            borrowing = Borrowing(
                user=user,
                book=book,
                expected_return_date=invalid_date,
            )
            with self.assertRaises(
                ValidationError, msg="Expected return date can't be in the past!"
            ):
                borrowing.clean()

    def test_cannot_borrow_book_if_inventory_is_zero(self):
        """
        Ensure that borrowing a book with zero inventory is not allowed.
        """
        book_out_of_stock = self.base_setup.book_out_of_stock
        borrowing = Borrowing(
            user=self.base_setup.user,
            book=book_out_of_stock,
            expected_return_date=datetime.date.today() + datetime.timedelta(days=5),
        )
        with self.assertRaises(
            ValidationError, msg=f"The book {book_out_of_stock.title} is out of stock!"
        ):
            borrowing.clean()

    def test_days_to_pay_for(self):
        """
        Ensure that days_to_pay_for() returns the correct number of days.
        """
        borrowing = self.base_setup.active_borrowing
        expected_days = (borrowing.expected_return_date - borrowing.borrow_date).days
        self.assertEqual(borrowing.days_to_pay_for(), expected_days)

    def test_total_price_calculation(self):
        """
        Ensure that total_price() calculates the correct total amount.
        """
        borrowing = self.base_setup.active_borrowing
        expected_price = borrowing.days_to_pay_for() * borrowing.book.daily_fee * 100
        self.assertEqual(borrowing.total_price(), expected_price)
