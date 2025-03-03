from rest_framework.test import APIClient
from django.test import TestCase
import datetime

from book.models import Author, Book
from borrowing.models import Borrowing
from payment.models import Payment
from user.models import User


class BaseSetUpForTest(TestCase):
    def setUp(self):
        today = datetime.date.today()

        # Create users
        self.admin_user = User.objects.create_superuser(
            email="admin@test.com", password="testpass123"
        )
        self.user = User.objects.create_user(
            email="user@test.com", password="testpass123"
        )

        # Create an author
        self.author = Author.objects.create(first_name="Test", last_name="Author")

        # Create available book
        self.book_available = Book.objects.create(
            title="Available Book",
            cover=Book.CoverType.HARD,
            inventory=10,
            daily_fee=9.99,
        )
        self.book_available.authors.add(self.author)

        # Create out-of-stock book
        self.book_out_of_stock = Book.objects.create(
            title="Out of Stock Book",
            cover=Book.CoverType.SOFT,
            inventory=0,  # No copies available
            daily_fee=7.50,
        )
        self.book_out_of_stock.authors.add(self.author)

        # Create borrowing that is expired
        self.expired_borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book_available,
            borrow_date=today - datetime.timedelta(days=10),
            expected_return_date=today - datetime.timedelta(days=5),
            actual_return_date=None,  # Not returned yet
        )

        # Create an active borrowing (not expired)
        self.active_borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book_available,
            borrow_date=today - datetime.timedelta(days=3),
            expected_return_date=today + datetime.timedelta(days=4),
            actual_return_date=None,
        )

        # Create a pending payment
        self.pending_payment = Payment.objects.create(
            borrowing=self.active_borrowing,
            status=Payment.Status.PENDING,
            amount=999,  # 9.99 in cents
            payment_type=Payment.Type.PAYMENT,
        )

        # API client for authentication
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
