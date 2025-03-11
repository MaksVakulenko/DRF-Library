from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from book.models import Book, Author
from borrowing.models import Borrowing
from payment.models import Payment
import datetime

User = get_user_model()


class BaseBorrowingTestCase(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        self.user = User.objects.create_user(email="user@example.com", password="testpass123")
        self.api_client.force_authenticate(user=self.user)

        self.author = Author.objects.create(first_name="John", last_name="Doe")

        self.book = Book.objects.create(
            title="Test Book",
            cover=Book.CoverType.HARD,
            inventory=1,
            daily_fee=5.00,
        )

        self.book.authors.set([self.author])

        self.borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date=datetime.date.today() + datetime.timedelta(days=7),
        )

        self.payment = Payment.objects.create(
            borrowing=self.borrowing,
            session_url="https://stripe.com/test-session",
            session_id="test_session_id",
            amount_of_money=500,
            status=Payment.Status.PENDING,
            type=Payment.Type.PAYMENT,
        )
