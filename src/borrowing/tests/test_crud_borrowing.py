import datetime
from django.test import TestCase
from django.urls import reverse
from borrowing.models import Borrowing
from book.models import Book, Author
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class BorrowingCRUDTest(TestCase):
    """Test CRUD operations for Borrowing model."""

    def setUp(self):
        """Set up test data for Borrowing CRUD tests."""
        self.client = APIClient()
        self.user = User.objects.create_user(email="valid_user@example.com", password="testpass123")
        self.client.force_authenticate(self.user)

        self.author = Author.objects.create(first_name="John", last_name="Doe")

        self.book = Book.objects.create(
            title="Valid Test Book",
            cover=Book.CoverType.HARD,
            inventory=5,
            daily_fee=1.50
        )
        self.book.authors.add(self.author)

        self.borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date=datetime.date.today() + datetime.timedelta(days=7)
        )

    def test_successful_borrowing_creation(self):
        """Ensure borrowing is created when all validators pass."""
        borrowing = Borrowing(
            user=self.user,
            book=self.book,
            expected_return_date=datetime.date.today() + datetime.timedelta(days=7)
        )

        try:
            borrowing.full_clean()
        except Exception as e:
            self.fail(f"Borrowing.full_clean() raised an unexpected exception: {e}")

        borrowing.save()
        self.assertEqual(Borrowing.objects.count(), 2)
        self.assertEqual(borrowing.book, self.book)
        self.assertEqual(borrowing.user, self.user)
        self.assertIsNone(borrowing.actual_return_date)

    def test_list_borrowings(self):
        """Ensure user can list their borrowings."""
        response = self.client.get(reverse("borrowing:borrowing-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.borrowing.id)
        self.assertEqual(response.data[0]["book"], str(self.borrowing.book))
        self.assertEqual(response.data[0]["user"], self.user.email)

    def test_retrieve_borrowing(self):
        """Ensure user can retrieve a single borrowing."""
        response = self.client.get(reverse("borrowing:borrowing-detail", args=[self.borrowing.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.borrowing.id)
        self.assertEqual(response.data["book"]["title"], self.book.title)
        self.assertEqual(response.data["user"], self.user.email)
