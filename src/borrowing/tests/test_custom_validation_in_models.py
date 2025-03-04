import datetime
from unittest.mock import patch

from django.core.exceptions import ValidationError
from borrowing.models import Borrowing
from borrowing.tests.base_setup import BaseBorrowingTestCase
from payment.models import Payment
from user.models import User
from rest_framework.test import APIClient



class BorrowingValidationTest(BaseBorrowingTestCase):
    """Tests Borrowing model custom validation in real-world cases."""

    def test_user_cannot_borrow_with_expired_borrowing(self):
        """User should not be able to borrow a book if they have an expired borrowing."""
        self.borrowing.expected_return_date = datetime.date.today() - datetime.timedelta(days=1)
        self.borrowing.save()

        new_borrowing = Borrowing(
            user=self.user,
            book=self.book,
            expected_return_date=datetime.date.today() + datetime.timedelta(days=7),
        )

        with self.assertRaises(ValidationError) as context:
            new_borrowing.save()

        self.assertIn("You have an expired borrowing!", str(context.exception))

    def test_user_cannot_borrow_if_book_out_of_stock(self):
        """User should not be able to borrow if the book is out of stock."""
        self.book.inventory = 0
        self.book.save()

        user_without_debts = User.objects.create_user(email="clean_user@example.com", password="testpass123")

        new_borrowing = Borrowing(
            user=user_without_debts,
            book=self.book,
            expected_return_date=datetime.date.today() + datetime.timedelta(days=7),
        )

        with self.assertRaises(ValidationError) as context:
            new_borrowing.save()

        self.assertIn(f"The book {self.book.title} is out of stock!", str(context.exception))

    def test_cannot_borrow_with_expected_return_date_today(self):
        """Expected return date must be at least one day after borrowing date."""
        new_borrowing = Borrowing(
            user=self.user,
            book=self.book,
            expected_return_date=datetime.date.today(),
        )

        with self.assertRaises(ValidationError) as context:
            new_borrowing.save()

        self.assertIn("You have to borrow the book for at least one day!", str(context.exception))

    def test_cannot_borrow_with_expected_return_date_in_past(self):
        """Expected return date cannot be in the past."""
        past_date = datetime.date.today() - datetime.timedelta(days=2)

        new_borrowing = Borrowing(
            user=self.user,
            book=self.book,
            expected_return_date=past_date,
        )

        with self.assertRaises(ValidationError) as context:
            new_borrowing.save()

        self.assertIn("Expected return date can't be in the past!", str(context.exception))

    def test_user_cannot_borrow_with_pending_payment(self):
        """User should not be able to borrow if they have a pending payment."""
        Payment.objects.create(
            borrowing=self.borrowing,
            session_id="test_session",
            session_url="http://test.com",
            amount_of_money=1000,
            status=Payment.Status.PENDING,
            type=Payment.Type.PAYMENT,
        )

        new_borrowing = Borrowing(
            user=self.user,
            book=self.book,
            expected_return_date=datetime.date.today() + datetime.timedelta(days=7),
        )

        with self.assertRaises(ValidationError) as context:
            new_borrowing.save()

        self.assertIn("You have a pending payment!", str(context.exception))


    @patch("payment.models.Payment.create_stripe_checkout")
    def test_fine_is_applied_if_book_is_returned_late(self, mock_create_stripe_checkout):
        """If book is returned late, fine should be correctly applied."""

        self.borrowing.expected_return_date = datetime.date.today() - datetime.timedelta(days=5)
        self.borrowing.actual_return_date = None
        self.borrowing.save()


        api_client = APIClient()
        api_client.force_authenticate(user=self.user)

        mock_create_stripe_checkout.return_value = "http://mock-payment-url.com"

        response = api_client.post(f"/api/borrowings/{self.borrowing.id}/return/")

        self.assertEqual(response.status_code, 200)

        self.assertIn("redirect_url", response.data)

        mock_create_stripe_checkout.assert_called_once()

