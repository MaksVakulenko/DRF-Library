from rest_framework.test import APIClient
from django.test import TestCase

from book.models import Author, Book
from user.models import User


class BaseSetUpForTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            email="admin@test.com", password="testpass123"
        )

        self.user = User.objects.create_user(
            email="user@test.com", password="testpass123"
        )

        self.author = Author.objects.create(first_name="Test", last_name="Author")

        self.book = Book.objects.create(
            title="Test Book", cover=Book.CoverType.HARD, inventory=10, daily_fee=9.99
        )

        self.book.authors.add(self.author)

        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
